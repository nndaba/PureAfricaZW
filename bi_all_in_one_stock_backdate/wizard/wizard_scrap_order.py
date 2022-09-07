# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime,date, timedelta
from odoo.tools import float_compare

class WizardScrapOrder(models.TransientModel):
	_name = 'wizard.scrap.order.backdate'
	_description="Wizard Scrap Order Backdate"

	scrap_backdate = fields.Datetime('Backdate',required=True)
	scrap_remarks = fields.Char('Remarks', required=True)

	def scrap_order_confirm(self):
		if self.scrap_backdate >= datetime.now():
			raise UserError(_('Please Enter Correct Back Date'))
		
		if self._context.get('scrap_id'):
			stock_scrap_id = self.env['stock.scrap'].browse(self._context.get('scrap_id'))
			stock_scrap_id.with_context(scrap_backdate=self.scrap_backdate).do_scrap()
			stock_scrap_id.write({'date_done':self.scrap_backdate,'move_remarks_scrap':self.scrap_remarks})
			for stock_scrap_move in stock_scrap_id.move_id:
				stock_scrap_move.with_context(scrap_backdate=self.scrap_backdate).write({'date':self.scrap_backdate,'move_remark':self.scrap_remarks})
				for value in stock_scrap_move.stock_valuation_layer_ids:
					self.env.cr.execute("""UPDATE stock_valuation_layer SET create_date=%s,product_id=%s,stock_move_id=%s,company_id=%s WHERE id=%s""" ,(self.scrap_backdate,value.product_id.id,value.stock_move_id.id,value.company_id.id,value.id))
				
				if stock_scrap_id.product_id.categ_id.property_valuation != 'real_time':
					custom_accountmove = self.env['account.move'].create({'date':self.scrap_backdate,
						'journal_id':stock_scrap_move.product_id.categ_id.property_stock_journal.id,
						'stock_move_id':stock_scrap_move.id})
				for stock_scrap_move_line in stock_scrap_move.move_line_ids:
					stock_scrap_move_line.write({'date':self.scrap_backdate,
						'line_remark':self.scrap_remarks})



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:






