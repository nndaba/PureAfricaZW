# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime,date, timedelta
from odoo.tools.float_utils import float_compare, float_is_zero, float_round


class WizardManufacturingTransfer(models.TransientModel):
	_name = 'wizard.validate.manufacturing.transfer'

	transfer_date = fields.Datetime('BackDate',required=True)
	transfer_remark = fields.Char('Remark',required=True)


	def custom_backdateorder_button(self):
		if self.transfer_date >= datetime.now():
			raise UserError(_('Please Enter Correct Back Date'))

		active_models = self._context.get('active_model')
		if active_models == 'mrp.production':
			if self._context.get('mrp_id'):
				custom_mrp_prod = self.env['mrp.production'].browse(self._context.get('mrp_id'))
				
				custom_mrp_prod._button_mark_done_sanity_checks()
				if not self.env.context.get('button_mark_done_production_ids'):
					self = self.with_context(button_mark_done_production_ids=self.ids)
				res = custom_mrp_prod._pre_button_mark_done()
				if res is not True:
					return res
				
				
				custom_mrp_prod.button_mark_done()
				
				for mrp in custom_mrp_prod:
					mrp.write({'line_remark':self.transfer_remark})
					for raw_move in mrp.move_raw_ids:
						raw_move.write({'move_remark':self.transfer_remark,
							'date':self.transfer_date})
						for move_line in raw_move.move_line_ids:
							move_line.write({'date':raw_move.date,
								'line_remark':self.transfer_remark})
						for value in raw_move.stock_valuation_layer_ids:
							self.env.cr.execute("""UPDATE stock_valuation_layer SET create_date=%s,product_id=%s,stock_move_id=%s,company_id=%s WHERE id=%s""" ,(self.transfer_date,value.product_id.id,value.stock_move_id.id,value.company_id.id,value.id))

						for category in raw_move.product_id.categ_id:
							if category.property_valuation != 'real_time':

								accountmove = self.env['account.move'].create({'date':self.transfer_date,
										'journal_id':raw_move.product_id.categ_id.property_stock_journal.id,
										'stock_move_id':raw_move.id})

					if mrp.product_id.categ_id.property_valuation == 'real_time':
						for finished_move in mrp.move_finished_ids:
							finished_move.write({'move_remark':self.transfer_remark,
								'date':self.transfer_date})
							for value in finished_move.stock_valuation_layer_ids:
								self.env.cr.execute("""UPDATE stock_valuation_layer SET create_date=%s,product_id=%s,stock_move_id=%s,company_id=%s WHERE id=%s""" ,(self.transfer_date,value.product_id.id,value.stock_move_id.id,value.company_id.id,value.id))

						for account_move in custom_mrp_prod.move_raw_ids:
							result = self.env['account.move'].search([('stock_move_id','=',account_move.id)])
							result.write({'date':finished_move.date})

						results = self.env['account.move'].search([('stock_move_id','=',finished_move.id)])
						results.write({'date':raw_move.date})
					else:
						for finished_move in mrp.move_finished_ids:
							finished_move.write({'move_remark':self.transfer_remark,
												'date':self.transfer_date})
							for value in finished_move.stock_valuation_layer_ids:
								self.env.cr.execute("""UPDATE stock_valuation_layer SET create_date=%s,product_id=%s,stock_move_id=%s,company_id=%s WHERE id=%s""" ,(self.transfer_date,value.product_id.id,value.stock_move_id.id,value.company_id.id,value.id))

							custom_accountmove = self.env['account.move'].create({'date':self.transfer_date,
								'journal_id':finished_move.product_id.categ_id.property_stock_journal.id,
								'stock_move_id':finished_move.id})
					for finished_line in mrp.finished_move_line_ids:
						finished_line.write({'line_remark':self.transfer_remark,
							'date':self.transfer_date})
						
				
						
		elif active_models == 'stock.picking.type':
			custom_mrp_prod = self.env['mrp.production'].browse(self._context.get('active_id'))
			
			
			custom_mrp_prod._button_mark_done_sanity_checks()
			if not self.env.context.get('button_mark_done_production_ids'):
				self = self.with_context(button_mark_done_production_ids=self.ids)
			res = custom_mrp_prod._pre_button_mark_done()
			if res is not True:
				return res
			
			custom_mrp_prod.button_mark_done()
			
			for mrp in custom_mrp_prod:
				mrp.write({'line_remark':self.transfer_remark})
				for raw_move in mrp.move_raw_ids:
					raw_move.write({'move_remark':self.transfer_remark,
						'date':self.transfer_date})
					for value in raw_move.stock_valuation_layer_ids:
						self.env.cr.execute("""UPDATE stock_valuation_layer SET create_date=%s,product_id=%s,stock_move_id=%s,company_id=%s WHERE id=%s""" ,(self.transfer_date,value.product_id.id,value.stock_move_id.id,value.company_id.id,value.id))
  
					for move_line in raw_move.move_line_ids:
						move_line.write({'date':raw_move.date,
							'line_remark':self.transfer_remark})
						for category in raw_move.product_id.categ_id:
							if category.property_valuation != 'real_time':
								accountmove = self.env['account.move'].create({'date':self.transfer_date,
										'journal_id':raw_move.product_id.categ_id.property_stock_journal.id,
										'stock_move_id':raw_move.id})
  
				if mrp.product_id.categ_id.property_valuation == 'real_time':
					for finished_move in mrp.move_finished_ids:
						finished_move.write({'move_remark':self.transfer_remark,
							'date':self.transfer_date})
						for value in finished_move.stock_valuation_layer_ids:
							self.env.cr.execute("""UPDATE stock_valuation_layer SET create_date=%s,product_id=%s,stock_move_id=%s,company_id=%s WHERE id=%s""" ,(self.transfer_date,value.product_id.id,value.stock_move_id.id,value.company_id.id,value.id))

					for account_move in custom_mrp_prod.move_raw_ids:
  
						result = self.env['account.move'].search([('stock_move_id','=',account_move.id)])
						result.write({'date':finished_move.date})
					results = self.env['account.move'].search([('stock_move_id','=',finished_move.id)])
					results.write({'date':raw_move.date})
  
				else:
					for finished_move in mrp.move_finished_ids:
						finished_move.write({'move_remark':self.transfer_remark,
											'remark':self.transfer_remark,
											'date':self.transfer_date})
						for value in finished_move.stock_valuation_layer_ids:
							self.env.cr.execute("""UPDATE stock_valuation_layer SET create_date=%s,product_id=%s,stock_move_id=%s,company_id=%s WHERE id=%s""" ,(self.transfer_date,value.product_id.id,value.stock_move_id.id,value.company_id.id,value.id))
  
						custom_accountmove = self.env['account.move'].create({'date':self.transfer_date,
							'journal_id':finished_move.product_id.categ_id.property_stock_journal.id,
							'stock_move_id':finished_move.id})
  
				for finished_line in mrp.finished_move_line_ids:
					finished_line.write({'line_remark':self.transfer_remark,
						'date':self.transfer_date})
  
  
		elif active_models == 'stock.picking':
			custom_stock_picking_ids = self.env['stock.picking'].browse(self.env.context['active_id'])
			for picking in custom_stock_picking_ids.filtered(lambda x: x.state not in ('cancel')):
				for data in picking.move_lines:
					data.write({'date':self.transfer_date,'move_remark': self.transfer_remark,'move_date':self.transfer_date})
					for value in data.stock_valuation_layer_ids:
						self.env.cr.execute("""UPDATE stock_valuation_layer SET create_date=%s,product_id=%s,stock_move_id=%s,company_id=%s WHERE id=%s""" ,(self.transfer_date,value.product_id.id,value.stock_move_id.id,value.company_id.id,value.id))
					
					for category in data.product_id.categ_id:
						if category.property_valuation != 'real_time':
							custom_accountmove = self.env['account.move'].create({'date':self.transfer_date,'journal_id':data.product_id.categ_id.property_stock_journal.id,
								'ref':data.location_id.name,
								'stock_move_id':data.id})
					for line in data.mapped('move_line_ids'):
						line.write({'date': self.transfer_date,'line_remark':self.transfer_remark})
			return custom_stock_picking_ids.button_validate()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: