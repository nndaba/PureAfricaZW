# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PosConfig(models.Model):
    _inherit = 'pos.config'

    pos_bluetooth_printer = fields.Boolean('Bluetooth Printer', default=True)
    receipt_copies = fields.Integer('Copies of receipts', default=1)
    bluetooth_cashdrawer = fields.Boolean(string='Cashdrawer', help="Automatically open the cashdrawer.")
    receipt_types_views = fields.Selection(
        [('No', 'No'), ('categoryReceipt', 'Category Receipt'), ('labelReceipt', 'Label Receipt')], string="",
        default="No")
    is_different_printer = fields.Boolean('Use Different Bluetooth/USB/IP Printer')
    bluetooth_print_auto = fields.Boolean(string='Automatic Category/Label Printing', default=False,
                                          help='The Category/Label receipt will automatically be printed at the end of each order.')

    @api.onchange('pos_bluetooth_printer')
    def _onchange_ipos_bluetooth_printer(self):
        if not self.pos_bluetooth_printer:
            self.bluetooth_cashdrawer = False
            self.bluetooth_print_auto = False

    @api.onchange('iface_print_auto')
    def _onchange_iface_print_auto(self):
        if not self.iface_print_auto:
            self.bluetooth_print_auto = False