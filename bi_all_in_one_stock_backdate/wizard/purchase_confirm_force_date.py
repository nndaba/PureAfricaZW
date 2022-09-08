# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, exceptions, api, _
from datetime import datetime
from odoo.exceptions import Warning

class PurchaseOrder(models.Model):
    _inherit= 'purchase.order'
    
    def action_confirm_inherit(self):
        context = dict(self._context or {})
        data_obj = self.env['ir.model.data']

        return {
            'name': "Select Confirmation Force Date",
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'confirmation.date.wizard.purchase',
            'view_id': False,
            'context': context,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'nodestroy': True,
        }
        
        

class ConfirmDateWizard(models.TransientModel):
    _name = 'confirmation.date.wizard.purchase'
    _description = 'Confirmation Date Wizard'


    confirmation_force_date = fields.Datetime(string='Confirm Force Date', index=True, help="Date on which the sales order is confirmed.", copy=False)

    def action_confirm(self):
        context = dict(self._context) or {}
        if context.get('active_id', False):
            po_obj = self.env['purchase.order'].browse(context.get('active_id'))
            po_obj.button_confirm()
            po_obj.date_approve = self.confirmation_force_date
            picking = self.env['stock.picking'].search([('purchase_id', '=', po_obj.id), ('state', 'not in', ['cancel'])])
            if not po_obj.date_planned:
                for pic in picking:
                    picking.scheduled_date = self.confirmation_force_date
        return True

            
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
