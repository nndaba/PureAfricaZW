# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime,date, timedelta
from odoo.tools.float_utils import float_compare, float_is_zero, float_round

class StockUpdate(models.Model):
	_inherit = 'stock.move'

	move_date = fields.Date(string="Date")
	move_remark = fields.Char(string="Remarks")

	def _action_done(self,cancel_backorder=False):
		res = super(StockUpdate, self)._action_done()
		custom_stock_picking_ids = self.env['stock.picking'].browse(self._context.get('active_id'))
		stock_type_id = self.env['stock.picking.type'].browse(self._context.get('active_id'))
		active_models1 = self._context.get('active_model')
		if active_models1 == 'stock.picking.type':
			if stock_type_id.code != 'outgoing':
				for move in res:
					move.write({'date': move.move_date or fields.Datetime.now()})
					for line in move.mapped('move_line_ids'):
						line.write({'date': move.move_date or fields.Datetime.now()})
					for value in move.stock_valuation_layer_ids:
						self.env.cr.execute("""UPDATE stock_valuation_layer SET create_date=%s,product_id=%s,stock_move_id=%s,company_id=%s WHERE id=%s""" ,(move.move_date or fields.Datetime.now(),value.product_id.id,value.stock_move_id.id,value.company_id.id,value.id))
			elif stock_type_id.code == 'outgoing':
				for move in res:
					move.write({'date': move.move_date or fields.Datetime.now()})
					for line in move.mapped('move_line_ids'):
						line.write({'date': move.move_date or fields.Datetime.now()})
					for value in move.stock_valuation_layer_ids:
						self.env.cr.execute("""UPDATE stock_valuation_layer SET create_date=%s,product_id=%s,stock_move_id=%s,company_id=%s WHERE id=%s""" ,(move.move_date or fields.Datetime.now(),value.product_id.id,value.stock_move_id.id,value.company_id.id,value.id))

		elif active_models1 == 'stock.picking' :
			if custom_stock_picking_ids.picking_type_id.code != 'outgoing':
				for move in res:
					move.write({'date': move.move_date or fields.Datetime.now()})
					for line in move.mapped('move_line_ids'):
						line.write({'date': move.move_date or fields.Datetime.now()})
					for value in move.stock_valuation_layer_ids:
						self.env.cr.execute("""UPDATE stock_valuation_layer SET create_date=%s,product_id=%s,stock_move_id=%s,company_id=%s WHERE id=%s""" ,(move.move_date or fields.Datetime.now(),value.product_id.id,value.stock_move_id.id,value.company_id.id,value.id))

			elif custom_stock_picking_ids.picking_type_id.code =='outgoing':
				for move in res:
					move.write({'date': move.move_date or fields.Datetime.now()})
					for line in move.mapped('move_line_ids'):
						line.write({'date': move.move_date or fields.Datetime.now()})
					for value in move.stock_valuation_layer_ids:
						self.env.cr.execute("""UPDATE stock_valuation_layer SET create_date=%s,product_id=%s,stock_move_id=%s,company_id=%s WHERE id=%s""" ,(move.move_date or fields.Datetime.now(),value.product_id.id,value.stock_move_id.id,value.company_id.id,value.id))

		elif active_models1 == 'stock.scrap':
			for move in res:
				move.write({'date': move.move_date or fields.Datetime.now()})
				for line in move.mapped('move_line_ids'):
					line.write({'date': move.move_date or fields.Datetime.now()})
				for value in move.stock_valuation_layer_ids:
					self.env.cr.execute("""UPDATE stock_valuation_layer SET create_date=%s,product_id=%s,stock_move_id=%s,company_id=%s WHERE id=%s""" ,(move.move_date or fields.Datetime.now(),value.product_id.id,value.stock_move_id.id,value.company_id.id,value.id))

		elif active_models1 == 'purchase.order':
			for move in res:
				move.write({'date': move.move_date or fields.Datetime.now()})
				for line in move.mapped('move_line_ids'):
					line.write({'date': move.move_date or fields.Datetime.now()})
				for value in move.stock_valuation_layer_ids:
					self.env.cr.execute("""UPDATE stock_valuation_layer SET create_date=%s,product_id=%s,stock_move_id=%s,company_id=%s WHERE id=%s""" ,(move.move_date or fields.Datetime.now(),value.product_id.id,value.stock_move_id.id,value.company_id.id,value.id))

		elif active_models1 == 'sale.order':
			for move in res:
				move.write({'date': move.move_date or fields.Datetime.now()})
				for line in move.mapped('move_line_ids'):
					line.write({'date': move.move_date or fields.Datetime.now()})
				for value in move.stock_valuation_layer_ids:
					self.env.cr.execute("""UPDATE stock_valuation_layer SET create_date=%s,product_id=%s,stock_move_id=%s,company_id=%s WHERE id=%s""" ,(move.move_date or fields.Datetime.now(),value.product_id.id,value.stock_move_id.id,value.company_id.id,value.id))

		return res
		
	def _prepare_account_move_vals(self, credit_account_id, debit_account_id, journal_id, qty, description, svl_id, cost):
		self.ensure_one()
		AccountMove = self.env['account.move'].with_context(default_journal_id=journal_id)

		move_lines = self._prepare_account_move_line(qty, cost, credit_account_id, debit_account_id, description)

		if move_lines:
			
			if self._context.get('scrap_backdate'):
				date = self._context.get('scrap_backdate')
			elif self._context.get('transfer_date'):
				date = self._context.get('transfer_date')
			elif self._context.get('mrp_backdate'):
				date = self._context.get('mrp_backdate')
			elif self._context.get('inventory_date'):
				date = self._context.get('inventory_date')			
			else:
				date = self.move_date or self._context.get('force_period_date', fields.Date.context_today(self))
			return {
            'journal_id': journal_id,
            'line_ids': move_lines,
            'date': date,
            'ref': description,
            'stock_move_id': self.id,
            'stock_valuation_layer_ids': [(6, None, [svl_id])],
            'move_type': 'entry',
        }

class StockPickingIn(models.Model):
	_inherit = 'stock.picking'

	remark = fields.Char(string="Remarks")
	def button_validate_custom(self):
		custom = self.env['stock.picking'].browse(self.id)

		for order in self:

			if custom.picking_type_id.code in ('outgoing'):
				return {
						'name':'Process Backdate and Remarks',
						'view_type': 'form',
						'view_mode': 'form',
						'res_model': 'change.module',
						'type': 'ir.actions.act_window',
						'target': 'new',
						'res_id': False,
						'context': order.env.context,
					}

			elif custom.picking_type_id.code in ('internal','incoming'):
				return {
						'name':'Process Backdate and Remarks',
						'view_type': 'form',
						'view_mode': 'form',
						'res_model': 'wizard.validate.internal.transfer',
						'type': 'ir.actions.act_window',
						'target': 'new',
						'res_id': False,
						'context': order.env.context,
					}
			elif custom.picking_type_id.code == 'mrp_operation':
				return {
						'name':'Process Backdate and Remarks',
						'view_type': 'form',
						'view_mode': 'form',
						'res_model': 'wizard.validate.manufacturing.transfer',
						'type': 'ir.actions.act_window',
						'target': 'new',
						'res_id': False,
						'context': order.env.context,
					}

			else:
				return order.button_validate()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: