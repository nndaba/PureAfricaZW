# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from datetime import date,datetime
from odoo.exceptions import UserError, AccessError

class MassAssignBackdatePayment(models.Model):
	_name = 'mass.assign.backdate.payment.wizard'
	_description ='Mass Assign Backdate payment'


	payment_date= fields.Datetime(string="Payment Date" ,required=True)
	remarks = fields.Text(string="Remarks")
	account_payment_ids = fields.Many2many('account.payment')
	enable_payment=fields.Boolean(string='Enable Backdate For Payment',default=False)
	payment_remark=fields.Boolean(string='Enable Remark For Payment ',default=False)
	pay_remark=fields.Boolean(string='Remark Mandatory For Payment',default=False)

	@api.model
	def default_get(self, fields):
		res = super(MassAssignBackdatePayment, self).default_get(fields)
		active_ids = self._context.get('active_ids')
		enable_payment=self.env["ir.config_parameter"].sudo().get_param("bi_all_in_one_stock_backdate.enable_payment")
		payment_remark=self.env["ir.config_parameter"].sudo().get_param("bi_all_in_one_stock_backdate.payment_remark")
		pay_remark=self.env["ir.config_parameter"].sudo().get_param("bi_all_in_one_stock_backdate.pay_remark")
		res.update({
				'enable_payment': enable_payment,
				'payment_remark': payment_remark,
				'pay_remark':pay_remark,
		})
		return res  


    
	def invoice_backdate_payment_wizard(self):
		active_ids = self.env.context.get('active_ids')
		return{
				'name': 'Assign Backdate',
				'res_model': 'mass.assign.backdate.payment.wizard',
				'view_mode': 'form',
				'view_id': self.env.ref('bi_all_in_one_stock_backdate.wizard_mass_assign_backdate_payment').id,
				'context': {
					'default_account_payment_ids': [(6, 0, active_ids)],
				},
				'target': 'new',
				'type': 'ir.actions.act_window'
			}


	def on_click_confirm_payment(self):
		if self.payment_date >= datetime.now():
			raise UserError(_('Please Enter Correct Back Date'))
		for pay_id in self.env['res.config.settings'].sudo().search([],order="id desc", limit=1):
			if pay_id.enable_payment:
				for payment in self.account_payment_ids:

						if payment.state == 'posted':

							payment.action_draft()
							payment.name = False
							payment.write({
								'date' : self.payment_date,
								'remarks' : self.remarks
							})
							payment.action_post()
							payment.move_id.write({
								'remarks' : self.remarks
							})

						elif payment.state == 'cancel':

							payment.action_draft()
							payment.name = False
							payment.write({
								'date' : self.payment_date,
								'remarks' : self.remarks
							})
							payment.action_cancel()
							payment.move_id.write({
								'remarks' : self.remarks
							})
						
						else:

							payment.name = False
							payment.write({
								'date' : self.payment_date,
								'remarks' : self.remarks
							})
							payment.move_id.write({
								'remarks' : self.remarks
							})