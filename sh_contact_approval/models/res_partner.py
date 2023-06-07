# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ShContacts(models.Model):
    _inherit = 'res.partner'

    state = fields.Selection([
        ('draft', 'Draft'),
        ('under_approval', 'Under Approval'),
        ('approved', 'Approved'),
        ('not_approved', 'Not Approved')],
        default='draft',
        string="Status",
        required=True
    )

    is_first = fields.Boolean(default=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            res = super(ShContacts, self).create(vals)
            res.active = False
            res.state = 'under_approval'
            return res

    def write(self, vals):
        for rec in self:
            if vals.get('state') and vals.get('state') in ['approved']:
                if self.env.user.has_group('sh_contact_approval.sh_contact_approve_manager'):
                    vals.update({
                        'active': True
                    })
                else:
                    raise UserError(_("You are not Contact Manager"))
            elif vals.get('state') and vals.get('state') in ['not_approved']:
                if self.env.user.has_group('sh_contact_approval.sh_contact_approve_manager'):
                    vals.update({
                        'active': False
                    })
                else:
                    raise UserError(_("You are not Contact Manager"))
            elif vals.get('state') and vals.get('state') in ['under_approval']:
                if not self.is_first:
                    vals.update({
                        'active': False,
                        'is_first': True
                    })
                if self.is_first:
                    if self.env.user.has_group('sh_contact_approval.sh_contact_approve_manager'):
                        vals.update({
                            'active': False
                        })
                    else:
                        raise UserError(_("You are not Contact Manager"))

            elif vals.get('state') and vals.get('state') in ['draft']:
                if self.is_first:
                    if self.env.user.has_group('sh_contact_approval.sh_contact_approve_manager'):
                        vals.update({
                            'active': False
                        })
                    else:
                        raise UserError(_("You are not Contact Manager"))

        return super(ShContacts, self).write(vals)

    def approve_contact(self):
        user_id = self.env['res.users'].sudo().search(
            [('id', '=', self.env.user.id)], limit=1)
        if user_id.has_group('sh_contact_approval.sh_contact_approve_manager'):
            for rec in self:
                if rec.state in ['draft', 'not_approved', 'under_approval']:
                    # if rec.state in ['draft', 'not_approved', 'under_approval'] and not rec.active:
                    rec.state = 'approved'
                    rec.active = True
        else:
            raise UserError(_("You are not Contact Manager"))

    def not_approve_contact(self):
        user_id = self.env['res.users'].sudo().search(
            [('id', '=', self.env.user.id)], limit=1)
        if user_id.has_group('sh_contact_approval.sh_contact_approve_manager'):
            for rec in self:
                if rec.state in ['draft', 'under_approval', 'approved']:
                    # if rec.state in ['draft', 'under_approval', 'approved'] and rec.active:
                    rec.state = 'not_approved'
                    rec.active = False
        else:
            raise UserError(_("You are not Contact Manager"))
