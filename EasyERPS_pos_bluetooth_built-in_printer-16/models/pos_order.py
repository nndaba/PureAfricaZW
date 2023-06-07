# -*- encoding: utf-8 -*-

from odoo import api, fields, models

class OrderLine(models.Model):
    _inherit='pos.order.line'

    def _export_for_ui(self, orderline):
        result= super()._export_for_ui(orderline)
        desc=orderline.full_product_name.split('(')
        if len(desc)>1:
            desc=desc[1].replace(')','').strip()
            result['description'] =desc
        return result
