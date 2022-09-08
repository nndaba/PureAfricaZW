# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, _
from datetime import date,datetime
from odoo.exceptions import UserError, AccessError

class MassAssignBackdate(models.Model):
	_name = 'mass.assign.backdate.wizard'
	_description ='Mass Assign Backdate'


	invoice_date= fields.Datetime(string="Invoice Date" ,required=True)
	remarks = fields.Text(string="Remarks")
	account_move_ids = fields.Many2many('account.move')
	enable_backdate=fields.Boolean(string='Enable Backdate For Invoice',default=False)
	enable_remark=fields.Boolean(string='Enable Remark For Invoice ',default=False)
	inv_remark=fields.Boolean(string='Remark Mandatory For Invoice',default=False)


	@api.model
	def default_get(self, fields):
		res = super(MassAssignBackdate, self).default_get(fields)
		active_ids = self._context.get('active_ids')
		enable_backdate=self.env["ir.config_parameter"].sudo().get_param("bi_all_in_one_stock_backdate.enable_backdate")
		enable_remark=self.env["ir.config_parameter"].sudo().get_param("bi_all_in_one_stock_backdate.enable_remark")
		inv_remark=self.env["ir.config_parameter"].sudo().get_param("bi_all_in_one_stock_backdate.inv_remark")
		res.update({
				'enable_backdate': enable_backdate,
				'enable_remark': enable_remark,
				'inv_remark':inv_remark,
		})
		return res  


	def invoice_backdate_wizard(self):
		active_ids = self.env.context.get('active_ids')
		return{
				'name': 'Assign Backdate',
				'res_model': 'mass.assign.backdate.wizard',
				'view_mode': 'form',
				'view_id': self.env.ref('bi_all_in_one_stock_backdate.wizard_mass_assign_backdate').id,
				'context': {
					'default_account_move_ids': [(6, 0, active_ids)],
				},
				'target': 'new',
				'type': 'ir.actions.act_window'
			}

	def on_click_confirm(self):
		if self.invoice_date >= datetime.now():
			raise UserError(_('Please Enter Correct Back Date'))
		for pay_id in self.env['res.config.settings'].sudo().search([],order="id desc", limit=1):
			if pay_id.enable_backdate:
				self.account_move_ids.write({
					'invoice_date' : self.invoice_date,
					'remarks' : self.remarks
				})
				self.account_move_ids.line_ids.write({
					'date': self.invoice_date,
					'remarks' : self.remarks
				})

				
		   