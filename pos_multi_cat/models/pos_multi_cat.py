# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   License URL : <https://store.webkul.com/license.html/>
#
#################################################################################

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    pos_categ_id = fields.Many2many('pos.category', string='Point of Sale Categories')
