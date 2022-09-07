# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _



class AccountPayment(models.Model):
	_inherit = "account.payment"

	remarks = fields.Text(string="Remarks")

	