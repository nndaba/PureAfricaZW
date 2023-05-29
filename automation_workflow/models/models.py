from lxml import etree
from odoo import models, fields, api, _
import random
import string
import logging 

_logger = logging.getLogger(__name__)

class SaleOrderExtended(models.Model):
    _inherit = 'sale.order'

    sale_order_ref = fields.Char('Sale Order Reference')
    is_import = fields.Boolean(default=False)
    imported_invoice_count  = fields.Integer(default=1)

    @api.model
    def create(self, vals):
        if vals.get('is_import'):
            vals['sale_order_ref'] = ''.join(random.choices(string.digits, k=5))
        return super(SaleOrderExtended, self).create(vals)


    def view_invoice(self):
        if self.is_import:
            action = {
                'name': _('Account Move'),
                'domain': [('sale_order_ref','=',self.sale_order_ref)],
                'view_type': 'form',
                'res_model': 'account.move',
                'view_id': False,
                'view_mode':'tree,form',
                'type': 'ir.actions.act_window',
            }

            return action



class AccountMoveExtended(models.Model):
    _inherit = 'account.move'

    sale_order_ref = fields.Char('Sale Order Reference')

    @api.model
    def create(self, vals):
        if vals.get('invoice_origin'):
            sale_order = self.env['sale.order'].search([('name', '=', vals['invoice_origin'])])
            if sale_order.is_import and sale_order.sale_order_ref:
                vals['sale_order_ref'] = sale_order.sale_order_ref
        return super(AccountMoveExtended, self).create(vals)


class PurchaserOrderExtended(models.Model):
    _inherit = 'purchase.order'

    is_import = fields.Boolean(default=False)


