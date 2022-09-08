# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields , models , api , _
from ast import literal_eval
from odoo.exceptions import ValidationError
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT

class ResConfigSettings(models.TransientModel):
	_inherit = "res.config.settings"
	_description="Res config Settings"


	
	enable_backdate=fields.Boolean(string='Enable Backdate For Invoice',default=False)
	enable_remark=fields.Boolean(string='Enable Remark For Invoice ',default=False)
	inv_remark=fields.Boolean(string='Remark Mandatory For Invoice',default=False)
	enable_payment=fields.Boolean(string='Enable Backdate For Payment',default=False)
	payment_remark=fields.Boolean(string='Enable Remark For Payment ',default=False)
	pay_remark=fields.Boolean(string='Remark Mandatory For Payment',default=False)

	@api.model
	def get_values(self):
		res = super(ResConfigSettings, self).get_values()
		enable_backdate = self.env["ir.config_parameter"].sudo().get_param("bi_all_in_one_stock_backdate.enable_backdate")
		enable_remark = self.env["ir.config_parameter"].sudo().get_param("bi_all_in_one_stock_backdate.enable_remark")
		inv_remark = self.env["ir.config_parameter"].sudo().get_param("bi_all_in_one_stock_backdate.inv_remark")
		enable_payment = self.env["ir.config_parameter"].sudo().get_param("bi_all_in_one_stock_backdate.enable_payment")
		payment_remark = self.env["ir.config_parameter"].sudo().get_param("bi_all_in_one_stock_backdate.payment_remark")
		pay_remark = self.env["ir.config_parameter"].sudo().get_param("bi_all_in_one_stock_backdate.pay_remark")
		res.update(
			enable_backdate=enable_backdate,
			enable_remark=enable_remark,
			inv_remark =inv_remark,
			enable_payment = enable_payment,
			payment_remark = payment_remark,
			pay_remark = pay_remark,
		)
		return res

	def set_values(self):
	  res = super(ResConfigSettings, self).set_values()
	  config_env=self.env['ir.config_parameter'].sudo()
	  config_env.set_param("bi_all_in_one_stock_backdate.enable_backdate", self.enable_backdate)
	  config_env.set_param("bi_all_in_one_stock_backdate.enable_remark", self.enable_remark)
	  config_env.set_param("bi_all_in_one_stock_backdate.inv_remark", self.inv_remark)
	  config_env.set_param("bi_all_in_one_stock_backdate.enable_payment",self.enable_payment)
	  config_env.set_param("bi_all_in_one_stock_backdate.payment_remark",self.payment_remark)
	  config_env.set_param("bi_all_in_one_stock_backdate.pay_remark",self.pay_remark)

