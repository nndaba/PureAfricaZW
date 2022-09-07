# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _



class AccountMove(models.Model):
	_inherit = "account.move"

	remarks = fields.Text(string="Remarks")


class AccountMoveLine(models.Model):
	_inherit = "account.move.line"

	remarks = fields.Text(string="Remarks",related = "move_id.remarks")