# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime,date, timedelta

class InheritStockScrap(models.Model):
	_inherit = 'stock.scrap'

	move_remarks_scrap = fields.Char('Remarks')
	
	def action_validate(self):
		return {
					'name':'Process Backdate and Remarks',
					'view_type': 'form',
					'view_mode': 'form',
					'res_model': 'wizard.scrap.order.backdate',
					'type': 'ir.actions.act_window',
					'target': 'new',
					'res_id': False,
					'context': {
						'scrap_id': self.id,
					}
				}

	def do_scrap(self):
		self._check_company()
		for scrap in self:
			scrap.name = self.env['ir.sequence'].next_by_code('stock.scrap') or _('New')
			move = self.env['stock.move'].create(scrap._prepare_move_values())
			# master: replace context by cancel_backorder
			move.with_context(is_scrap=True,scrap_backdate=self._context.get('scrap_backdate'))._action_done()
			scrap.write({'move_id': move.id, 'state': 'done'})
			scrap.date_done = fields.Datetime.now()
		return True


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: