# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models,api, _
from odoo.exceptions import UserError, Warning, ValidationError
from odoo.tools.misc import get_lang
from odoo.osv import expression
from odoo.tools import float_is_zero, float_compare, float_round


class SaleOrder(models.Model):
    _inherit ='sale.order'
    
    sale_manual_currency_rate_active = fields.Boolean('Apply Manual Exchange')
    sale_manual_currency_rate = fields.Float('Rate', digits=(12, 6))


    def _prepare_invoice(self):
        res = super(SaleOrder,self)._prepare_invoice()
        res.update({'manual_currency_rate_active':self.sale_manual_currency_rate_active,'manual_currency_rate':self.sale_manual_currency_rate})
        return res;



class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'


    @api.onchange('product_id')
    def product_id_change(self):
        if not self.product_id:
            return
        valid_values = self.product_id.product_tmpl_id.valid_product_template_attribute_line_ids.product_template_value_ids
        # remove the is_custom values that don't belong to this template
        for pacv in self.product_custom_attribute_value_ids:
            if pacv.custom_product_template_attribute_value_id not in valid_values:
                self.product_custom_attribute_value_ids -= pacv

        # remove the no_variant attributes that don't belong to this template
        for ptav in self.product_no_variant_attribute_value_ids:
            if ptav._origin not in valid_values:
                self.product_no_variant_attribute_value_ids -= ptav

        vals = {}
        if not self.product_uom or (self.product_id.uom_id.id != self.product_uom.id):
            vals['product_uom'] = self.product_id.uom_id
            vals['product_uom_qty'] = self.product_uom_qty or 1.0

        product = self.product_id.with_context(
            lang=get_lang(self.env, self.order_id.partner_id.lang).code,
            partner=self.order_id.partner_id,
            quantity=vals.get('product_uom_qty') or self.product_uom_qty,
            date=self.order_id.date_order,
            pricelist=self.order_id.pricelist_id.id,
            uom=self.product_uom.id
        )

        vals.update(name=self.get_sale_order_line_multiline_description_sale(product))

        self._compute_tax_id()
        company = self.order_id.company_id

        if self.order_id.sale_manual_currency_rate_active:
            currency_rate = self.order_id.sale_manual_currency_rate/company.currency_id.rate
            price_unit = self.product_id.lst_price
            manual_currency_rate = price_unit * currency_rate            
            vals['price_unit'] = manual_currency_rate
            vals['name'] = self.product_id.name
        elif self.order_id.pricelist_id and self.order_id.partner_id:
            vals['price_unit'] = self.env['account.tax']._fix_tax_included_price_company(self._get_display_price(product), product.taxes_id, self.tax_id, self.company_id)
        
        self.update(vals)

        if product.sale_line_warn != 'no-message':
            if product.sale_line_warn == 'block':
                self.product_id = False

            return {
                'warning': {
                    'title': _("Warning for %s", product.name),
                    'message': product.sale_line_warn_msg,
                }
            }



    @api.onchange('product_uom', 'product_uom_qty')
    def product_uom_change(self):
        if not self.order_id.pricelist_id:
            raise UserError(_("Please Select Pricelist First."))
        if not self.product_uom or not self.product_id:
            self.price_unit = 0.0
            return
        if self.order_id.pricelist_id and self.order_id.partner_id:
            product = self.product_id.with_context(
                lang=self.order_id.partner_id.lang,
                partner=self.order_id.partner_id,
                quantity=self.product_uom_qty,
                date=self.order_id.date_order,
                pricelist=self.order_id.pricelist_id.id,
                uom=self.product_uom.id,
                fiscal_position=self.env.context.get('fiscal_position')
            )

        company = self.order_id.company_id
        if self.order_id.sale_manual_currency_rate_active:
            currency_rate = self.order_id.sale_manual_currency_rate/company.currency_id.rate
            price_unit = self.product_id.lst_price
            manual_currency_rate = price_unit * currency_rate
            self.price_unit = manual_currency_rate
            self.name = self.product_id.name
        else:
            self.price_unit = self.env['account.tax']._fix_tax_included_price_company(self._get_display_price(product), product.taxes_id, self.tax_id, self.company_id)
    

class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"


    def _create_invoice(self, order, so_line, amount):
        res = super(SaleAdvancePaymentInv,self)._create_invoice(order, so_line, amount)
        if order.sale_manual_currency_rate_active:
            res.write({'manual_currency_rate_active':order.sale_manual_currency_rate_active,'manual_currency_rate':order.sale_manual_currency_rate})
        return res

