from odoo import models, fields, api

class SaleOrderExtended(models.Model):
    _inherit = 'sale.order'

    sale_order_ref = fields.Char('sale_order_ref')
    is_import = fields.Boolean(default = False)

class PurchaserOrderExtended(models.Model):
    _inherit = 'purchase.order'

    is_import = fields.Boolean(default=False)

class AccountMoveExtended(models.Model):
    _inherit = 'account.move'

    sale_order_ref = fields.Char('sale_order_ref')