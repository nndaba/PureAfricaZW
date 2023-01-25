# -*- coding: utf-8 -*-

from os import write
from odoo import models, fields, api
import json
import requests
import datetime
from datetime import timedelta

# class fiscalization(models.Model):
#     _name = 'fiscalization.fiscalization'
#     _description = 'fiscalization.fiscalization'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100


class DialogBox(models.TransientModel):
    _name = 'fiscalization.dialog.box'

    title = fields.Char(string='Title', readonly=True)
    message = fields.Char(string='Message', readonly=True)


class account_move(models.Model):
    _name = 'account.move'
    _inherit = 'account.move'

    fiscal_signature = fields.Char(string='Signature')
    fiscal_date = fields.Datetime(string='Fiscalization Date')

    @api.model
    def handle_fiscalize(self, account_info):
        url = "http://154.119.80.13:3000/revmax/post"

        headers = {'Content-Type': 'application/json'}
        message = ""
        try:
            invoices = self.env['account.move'].search(
                [("id", "=", account_info[0]), ('state', '=', 'posted')])

            for invoice in invoices:

                if(len(str(invoice.fiscal_signature)) > 10):
                    message = "Already Fiscalized"
                    break

                lines = self.env['account.move.line'].search(
                    [('move_id', '=', invoice.id), ("exclude_from_invoice_tab", "=", False)])

                parsed_invoice = {
                    'invoice_id': invoice.id,
                    'invoice_number': invoice.name,
                    'customer_name': invoice.partner_id.name,
                    'address': invoice.partner_id.street,
                    'phone': invoice.partner_id.mobile,
                    'amount': invoice.amount_total,
                    'amount_tax': invoice.amount_tax,
                    'cashier': invoice.create_uid.name,
                    'comment': invoice.narration,
                    'currency': invoice.currency_id.name
                }

                _lines = []
                for line in lines:
                    parsed_line = {
                        'product_name': line.product_id.name,
                        'code': line.product_id.id,
                        'qty': line.quantity,
                        'price': line.price_unit,
                        'amount': line.price_total,
                        'tax': line.price_total - line.price_subtotal,
                        'tax_r': 0.145
                    }

                    _lines.append(parsed_line)

                data = {
                    'invoice': parsed_invoice,
                    'lines': _lines
                }

                resp = requests.post(url=url, json=data, headers=headers)

                if(resp.status_code == 200):
                    invoice.fiscal_signature = resp.content
                    invoice.fiscal_date = datetime.datetime.now()

                    message = invoice.fiscal_signature

                    self.env['mail.message'].create({
                        "subject": "Fiscalization",
                        "body": f'''
                            Fiscalization done
                                <br/><br/>
                            - By: {self.env.user.name}
                            <br/>
                            - Date: {subtract_two_hours(invoice.fiscal_date)}
                        ''',
                        "message_type": "comment",
                        "subtype_id": 1,
                        "author_id": self.env.user.id,
                        "model": "account.move",
                        "res_id": invoice.id,
                        "create_uid": self.env.user.id,
                        "write_uid": self.env.user.id
                    })

                else:
                    message = f"Failed to fiscalize: {resp.status_code}"

                break

        except Exception as e:

            message = f"Failed to fiscalize: {e}"

        finally:

            dialog = self.env['fiscalization.dialog.box'].create({
                'title': 'Fiscalization',
                'message': message,
            })

            return {
                'type': 'ir.actions.act_window',
                'res_model': 'fiscalization.dialog.box',
                'view_mode': 'form',
                'view_type': 'form',
                'res_id': dialog.id,
                'views': [(False, 'form')],
                'target': 'new',
            }

def subtract_two_hours(date_):

    time_ = date_ + timedelta(hours=2)

    return time_.strftime("%Y-%m-%d %H:%M:%S")
