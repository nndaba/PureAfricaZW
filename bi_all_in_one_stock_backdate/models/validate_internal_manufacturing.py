# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime,date, timedelta
from odoo.tools.float_utils import float_compare, float_is_zero, float_round		

class StockMoveUpdate(models.Model):
	_inherit = 'stock.move'

	move_date = fields.Date(string="Date")
	move_remark = fields.Char(string="Remarks")
class StockMoveLineInherit(models.Model):
	_inherit = 'stock.move.line'

	line_remark = fields.Char(string="Remark")

class ManufacturingInherit(models.Model):
	_inherit = 'mrp.production'

	
	line_remark = fields.Char(string="Remark")


	def button_done_mark(self):
		for order in self:
			return {
					'name':'Process Backdate and Remarks',
					'view_type': 'form',
					'view_mode': 'form',
					'res_model': 'wizard.validate.manufacturing.transfer',
					'type': 'ir.actions.act_window',
					'target': 'new',
					'res_id': False,
					'context': {
						'mrp_id': self.id,
					}
				}


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:





