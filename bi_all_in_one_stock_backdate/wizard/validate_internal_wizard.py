# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime,date, timedelta
from odoo.tools.float_utils import float_compare, float_is_zero, float_round

class WizardInternalTransfer(models.TransientModel):
	_name = 'wizard.validate.internal.transfer'
	_description='Wizard Validate Internal Transfer'

	transfer_date = fields.Datetime('BackDate',required=True)
	transfer_remark = fields.Char('Remark',required=True)


	def custom_backdate_button(self):
		if self.transfer_date >= datetime.now():
			raise UserError(_('Please Enter Correct Back Date'))
		
		active_models1 = self._context.get('active_model')
		if active_models1 == 'stock.picking':
			custom_stock_picking_ids = self.env['stock.picking'].browse(self._context.get('active_id'))
			for picking in custom_stock_picking_ids.filtered(lambda x: x.state not in ('cancel')):
				for data in picking.move_lines:
					data.write({'date':self.transfer_date,'move_remark': self.transfer_remark,'move_date':self.transfer_date})
					for value in data.stock_valuation_layer_ids:
						self.env.cr.execute("""UPDATE stock_valuation_layer SET create_date=%s,product_id=%s,stock_move_id=%s,company_id=%s WHERE id=%s""" ,(self.transfer_date,value.product_id.id,value.stock_move_id.id,value.company_id.id,value.id))
					
					accounts_data = data.product_id.product_tmpl_id.get_product_accounts()
					acc_valuation = accounts_data.get('stock_valuation', False)
					if custom_stock_picking_ids.picking_type_id.code == 'internal':
						for category in data.product_id.categ_id:
							if category.property_valuation != 'real_time':
								custom_accountmove = self.env['account.move'].create({'date':self.transfer_date,'journal_id':data.product_id.categ_id.property_stock_journal.id,
									'ref':data.location_id.name,
									'stock_move_id':data.id})
					elif custom_stock_picking_ids.picking_type_id.code == 'incoming':
						for category in data.product_id.categ_id:
							if category.property_valuation != 'real_time':
								custom_accountmove = self.env['account.move'].create({'date':self.transfer_date,'journal_id':data.product_id.categ_id.property_stock_journal.id,
									'ref':data.location_id.name,
									'stock_move_id':data.id})
					for line in data.mapped('move_line_ids'):
						line.write({'date': self.transfer_date,'line_remark':self.transfer_remark})
			return custom_stock_picking_ids.button_validate()

		elif active_models1 == 'stock.picking.type':
			custom_stock_picking_ids = self.env['stock.picking'].browse(self._context.get('active_id'))
			stock_type_id = self.env['stock.picking.type'].browse(self._context.get('active_id'))
			stock_picking_type = self.env['stock.picking'].search([('picking_type_id','=',stock_type_id.id)],
				order='id desc',limit=1)
			for picking in stock_picking_type:
				for data in picking.move_lines:
					data.write({'date':self.transfer_date,'move_remark': self.transfer_remark,'move_date':self.transfer_date})
					for value in data.stock_valuation_layer_ids:
						self.env.cr.execute("""UPDATE stock_valuation_layer SET create_date=%s,product_id=%s,stock_move_id=%s,company_id=%s WHERE id=%s""" ,(self.transfer_date,value.product_id.id,value.stock_move_id.id,value.company_id.id,value.id))
					
					for line in data.mapped('move_line_ids'):
						line.write({'date': self.transfer_date,'line_remark':self.transfer_remark})
					if stock_type_id.code == 'internal':
						for category in data.product_id.categ_id:
							if category.property_valuation != 'real_time':
								custom_accountmove = self.env['account.move'].create({'date':self.transfer_date,'journal_id':data.product_id.categ_id.property_stock_journal.id,
									'ref':data.location_id.name,
									'stock_move_id':data.id})
					elif stock_type_id.code == 'incoming':
						for category in data.product_id.categ_id:
							if category.property_valuation != 'real_time':
								custom_accountmove = self.env['account.move'].create({'date':self.transfer_date,'journal_id':data.product_id.categ_id.property_stock_journal.id,
									'ref':data.location_id.name,
									'stock_move_id':data.id})
			return stock_picking_type.button_validate()


		elif active_models1 == 'purchase.order':
			custom_stock_picking_ids = self.env['stock.picking'].browse(self._context.get('active_id'))
			custom_purchase_ids = self.env['purchase.order'].browse(self._context.get('active_id'))
			for custom_purchase_stock in self.env['stock.picking'].search([('purchase_id','=',custom_purchase_ids.id)]):
				for picking in custom_purchase_stock:
					for data in picking.move_lines:
						data.write({'move_remark':self.transfer_remark,'date':self.transfer_date,
							'move_date':self.transfer_date})
						for value in data.stock_valuation_layer_ids:
							self.env.cr.execute("""UPDATE stock_valuation_layer SET create_date=%s,product_id=%s,stock_move_id=%s,company_id=%s WHERE id=%s""" ,(self.transfer_date,value.product_id.id,value.stock_move_id.id,value.company_id.id,value.id))

						for line in data.mapped('move_line_ids'):
							line.write({'date': self.transfer_date,'line_remark':self.transfer_remark})
						for category in data.product_id.categ_id:
							if category.property_valuation != 'real_time':
								custom_accountmove = self.env['account.move'].create({'date':self.transfer_date,
									'journal_id':data.product_id.categ_id.property_stock_journal.id,
									'ref':data.location_id.name,
									'stock_move_id':data.id})
				return custom_purchase_stock.button_validate()



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: