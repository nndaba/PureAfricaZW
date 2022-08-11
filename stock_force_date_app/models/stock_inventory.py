# -*- coding: utf-8 -*-

import time
from odoo import api, fields, models, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.float_utils import float_compare, float_is_zero
from odoo.exceptions import UserError, ValidationError


class StockQuant(models.Model):
	_inherit = 'stock.quant'

	force_date = fields.Datetime(string="Force Date")


	@api.model
	def _get_inventory_fields_create(self):
		""" Returns a list of fields user can edit when he want to create a quant in `inventory_mode`.
		"""
		return ['product_id', 'location_id', 'lot_id', 'package_id', 'owner_id','force_date'] + self._get_inventory_fields_write()

	@api.model
	def _get_inventory_fields_write(self):
		""" Returns a list of fields user can edit when he want to edit a quant in `inventory_mode`.
		"""
		fields = ['inventory_quantity', 'inventory_quantity_auto_apply', 'inventory_diff_quantity',
				  'inventory_date', 'user_id', 'inventory_quantity_set', 'is_outdated', 'force_date']
		return fields

	@api.model
	def create(self, vals):
		""" Override to handle the "inventory mode" and create a quant as
		superuser the conditions are met.
		"""
		if self._is_inventory_mode() and any(f in vals for f in ['inventory_quantity', 'inventory_quantity_auto_apply']):
			allowed_fields = self._get_inventory_fields_create()
			if not self.user_has_groups('stock_force_date_app.group_stock_force_date'):
				if any(field for field in vals.keys() if field not in allowed_fields):
					raise UserError(_("Quant's creation is restricted, you can't do this operation."))

			inventory_quantity = vals.pop('inventory_quantity', False) or vals.pop(
				'inventory_quantity_auto_apply', False) or 0
			# Create an empty quant or write on a similar one.
			product = self.env['product.product'].browse(vals['product_id'])
			location = self.env['stock.location'].browse(vals['location_id'])
			lot_id = self.env['stock.production.lot'].browse(vals.get('lot_id'))
			package_id = self.env['stock.quant.package'].browse(vals.get('package_id'))
			owner_id = self.env['res.partner'].browse(vals.get('owner_id'))
			quant = self._gather(product, location, lot_id=lot_id, package_id=package_id, owner_id=owner_id, strict=True)

			if quant:
				quant = quant[0].sudo()
			else:
				quant = self.sudo().create(vals)
			# Set the `inventory_quantity` field to create the necessary move.
			quant.inventory_quantity = inventory_quantity
			quant.user_id = vals.get('user_id', self.env.user.id)
			quant.inventory_date = fields.Date.today()

			return quant
		res = super(StockQuant, self).create(vals)
		if self._is_inventory_mode():
			res._check_company()
		return res

	def _get_inventory_move_values(self, qty, location_id, location_dest_id, out=False):
		res = super(StockQuant, self)._get_inventory_move_values(qty, location_id, location_dest_id, out=False)
		if res:
			if self.force_date:
				res.update({'date': self.force_date})
			else:
				res.update({'date': self.in_date})
		return res


	def _apply_inventory(self):
		move_vals = []
		if not self.user_has_groups('stock.group_stock_manager'):
			raise UserError(_('Only a stock manager can validate an inventory adjustment.'))
		for quant in self:
			# Create and validate a move so that the quant matches its `inventory_quantity`.
			if float_compare(quant.inventory_diff_quantity, 0, precision_rounding=quant.product_uom_id.rounding) > 0:
				move_vals.append(
					quant._get_inventory_move_values(quant.inventory_diff_quantity,
													 quant.product_id.with_company(quant.company_id).property_stock_inventory,
													 quant.location_id))
			else:
				move_vals.append(
					quant._get_inventory_move_values(-quant.inventory_diff_quantity,
													 quant.location_id,
													 quant.product_id.with_company(quant.company_id).property_stock_inventory,
													 out=True))
		moves = self.env['stock.move'].with_context(inventory_mode=False).create(move_vals)
		if self.env.user.has_group('stock_force_date_app.group_stock_force_date'):
			for quant in self:
				moves = self.env['stock.move'].with_context(inventory_mode=False, force_date=quant.force_date).create(move_vals)
		moves._action_done()
		self.location_id.write({'last_inventory_date': fields.Date.today()})
		date_by_location = {loc: loc._get_next_inventory_date() for loc in self.mapped('location_id')}
		for quant in self:
			quant.inventory_date = date_by_location[quant.location_id]
		self.write({'inventory_quantity': 0, 'user_id': False})
		self.write({'inventory_diff_quantity': 0})


class StockPicking(models.Model):
	_inherit = 'stock.picking'

	force_date = fields.Datetime(string="Force Date")


class StockMove(models.Model):
	_inherit = 'stock.move'

	def _action_done(self, cancel_backorder=False):
		force_date = time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
		if self.env.user.has_group('stock_force_date_app.group_stock_force_date'):
			for move in self:
				if self._context.get('force_date'):
					force_date = self._context.get('force_date')
				if move.picking_id:
					if move.picking_id.force_date:
						force_date = move.picking_id.force_date
					else:
						force_date = move.picking_id.scheduled_date
		res = super(StockMove, self)._action_done(cancel_backorder=cancel_backorder)
		if self.env.user.has_group('stock_force_date_app.group_stock_force_date'):
			if force_date:
				for move in res:
					move.write({'date':force_date})
					if move.move_line_ids:
						for move_line in move.move_line_ids:
							move_line.write({'date':force_date})
					if move.account_move_ids:
						for account_move in move.account_move_ids:
							self.env.cr.execute(
            						"UPDATE account_move SET date = %s WHERE id = %s",
            							[force_date, account_move.id])
							# account_move.write({'date':force_date})
		return res


	def _create_account_move_line(self, credit_account_id, debit_account_id, journal_id, qty, description, svl_id, cost):
		self.ensure_one()
		AccountMove = self.env['account.move'].with_context(default_journal_id=journal_id)

		move_lines = self._prepare_account_move_line(qty, cost, credit_account_id, debit_account_id, description)
		if move_lines:
			date = self._context.get('force_period_date', fields.Date.context_today(self))
			if self.env.user.has_group('stock_force_date_app.group_stock_force_date'):
				if self.picking_id.force_date:
					date = self.picking_id.force_date.date()
			new_account_move = AccountMove.sudo().create({
				'journal_id': journal_id,
				'line_ids': move_lines,
				'date': date,
				'ref': description,
				'stock_move_id': self.id,
				'stock_valuation_layer_ids': [(6, None, [svl_id])],
				'move_type': 'entry',
			})
			new_account_move._post()