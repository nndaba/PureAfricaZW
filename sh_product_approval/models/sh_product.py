# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ShProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model
    def create(self, vals):
        res = super(ShProductTemplate, self).create(vals)
        for product in res.product_variant_ids:
            product.active = False
            product.state = "under_approval"
        res.active = False
        return res


class ShProduct(models.Model):
    _inherit = "product.product"

    state = fields.Selection([
        ("draft", "Draft"),
        ("under_approval", "Under Approval"),
        ("not_approved", "Not Approved"),
        ("approved", "Approved"),
    ],
        default="draft",
        string="State", required=True)

    def approve_product(self):
        user_id = self.env["res.users"].sudo().search(
            [("id", "=", self.env.user.id)], limit=1)
        if user_id.has_group("sh_product_approval.sh_product_approve_manager"):
            for rec in self:
                if rec.state in ["draft", "not_approved", "under_approval"]:
                    rec.state = "approved"
                    rec.active = True
                    rec.product_tmpl_id.active = True
        else:
            raise UserError(_("You are not Product Manager"))

    def not_approve_product(self):
        user_id = self.env["res.users"].sudo().search(
            [("id", "=", self.env.user.id)], limit=1)
        if user_id.has_group("sh_product_approval.sh_product_approve_manager"):
            for rec in self:
                if rec.state in ["draft", "under_approval", "approved"]:
                    rec.state = "not_approved"
                    rec.active = False
                    rec.product_tmpl_id.active = False
        else:
            raise UserError(_("You are not Product Manager"))

    @api.model
    def create(self, vals):
        if vals.get("state", False) in ["draft"]:
            vals.update({
                "active": False,
                "state": "under_approval",
            })
        return super(ShProduct, self).create(vals)

    def write(self, vals):
        if self:
            if(
                vals.get("state") in ["approved", "under_approval", "not_approved"] and
                self.state in ["draft", "approved", "under_approval", "not_approved"] and
                self.active
            ):
                vals.update({
                    "active": False
                })
            elif(
                vals.get("state") in ["approved", "under_approval", "not_approved"] and
                self.state in ["draft", "under_approval", "not_approved"] and not
                self.active
            ):
                vals.update({
                    "active": True
                })
        return super(ShProduct, self).write(vals)
