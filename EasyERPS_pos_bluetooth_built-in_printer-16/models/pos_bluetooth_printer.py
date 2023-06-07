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

    @api.onchange('pos_iface_print_auto')
    def _onchange_iface_print_auto(self):
        if not self.pos_iface_print_auto:
            self.bluetooth_print_auto = False

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    pos_bluetooth_printer = fields.Boolean(related='pos_config_id.pos_bluetooth_printer', readonly=False)
    receipt_copies = fields.Integer(related='pos_config_id.receipt_copies', readonly=False)
    bluetooth_cashdrawer = fields.Boolean(string='Cashdrawer', help="Automatically open the cashdrawer.")
    receipt_types_views = fields.Selection(related='pos_config_id.receipt_types_views', readonly=False)
    is_different_printer = fields.Boolean(related='pos_config_id.is_different_printer', readonly=False)
    bluetooth_print_auto = fields.Boolean(related='pos_config_id.bluetooth_print_auto', readonly=False)

    @api.onchange('pos_bluetooth_printer')
    def _onchange_ipos_bluetooth_printer(self):
        if not self.pos_bluetooth_printer:
            self.bluetooth_cashdrawer = False
            self.bluetooth_print_auto = False

    @api.onchange('pos_iface_print_auto')
    def _onchange_iface_print_auto(self):
        if not self.pos_iface_print_auto:
            self.bluetooth_print_auto = False