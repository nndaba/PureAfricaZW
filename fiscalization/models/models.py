# -*- coding: utf-8 -*-

from os import write
from odoo import models, fields, api
import json
import requests
import datetime
from datetime import timedelta
from odoo.exceptions import ValidationError

import logging

_logger = logging.getLogger(__name__)



class DialogBox(models.TransientModel):
    _name = 'fiscalization.dialog.box'

    title = fields.Char(string='Title', readonly=True)
    message = fields.Char(string='Message', readonly=True)

# class ResCompany(models.Model):
#     _inherit = 'res.company'
    
#     bp_number = fields.Char(string='BP Number')
#     tin_number = fields.Char(string='TIN Number')
    
    

class account_move(models.Model):
    _inherit = 'account.move'
    
    bp_number = fields.Char(string='BP Number')
    vat = fields.Char(string='Vat Number')
    customer_tin = fields.Char(string='Customer TIN')

    fiscal_signature = fields.Char(string='Signature')
    fiscal_date = fields.Datetime(string='Fiscalization Date')
    device_id = fields.Char(string='Device Id')
    rgn = fields.Char(string='Receipt Global Number')
    receiptnumber = fields.Char(string='Receipt number')
    fiscalday = fields.Char(string='Fiscal Day')
    VerificationCode = fields.Char(string='VerificationCode')
    
            
    @api.model
    def handle_fiscalize(self, account_info):
        url = "http://196.27.106.118:3000/revmax/post"

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
                    [('move_id', '=', invoice.id),("quantity", ">", 0)])
                
                reverse_entry = ''
                if invoice.move_type == 'out_refund':
                    reverse = invoices = self.env['account.move'].search(
                    [("id", "=", invoice.reversed_entry_id.id)])
                    reverse_entry = reverse.name

                else:
                    pass
                

                parsed_invoice = {
                    'invoice_id': invoice.id,
                    'invoice_number': invoice.name,
                    'customer_name': invoice.partner_id.name,
                    'customer_vat': invoice.partner_id.vat,
                    'customer_tin': invoice.partner_id.x_studio_tin_number,
                    'address': invoice.partner_id.street,
                    'phone': invoice.partner_id.mobile,
                    'amount': invoice.amount_total,
                    'amount_tax': invoice.amount_tax,
                    'cashier': invoice.create_uid.name,
                    'comment': invoice.narration,
                    'currency': invoice.currency_id.name,
                    'invoicestatus': invoice.move_type,
                    'ref': reverse_entry,
                    'amount_untaxed' : invoice.amount_untaxed
                }

                _lines = []
                records = []
                for line in lines:

                    self.env.cr.execute("""
                        SELECT at.id, at.name, at.amount
                        FROM account_tax at
                        JOIN account_move_line_account_tax_rel amltr ON at.id = amltr.account_tax_id
                        WHERE amltr.account_move_line_id = %s
                    """, (line.id,))

                    
                    tax_records = self.env.cr.fetchall()
                    records.append(tax_records)
                    raise ValidationError(records)

                    _logger.info(45*'$')
                    _logger.info(f'tax_records = {tax_records}')
                    _logger.info(45*'$')
                    

                    
                    parsed_line = {
                        'product_name': line.product_id.name,
                        'code': line.product_id.id,
                        'qty': line.quantity,
                        'price': line.price_unit,
                        'amount': line.price_total,
                        'tax': line.price_total - line.price_subtotal,
                        'tax_r': 0.15
                    }

                    _lines.append(parsed_line)

                data = {
                    'invoice': parsed_invoice,
                    'lines': _lines
                }

                resp = requests.post(url=url, json=data, headers=headers)
                values = resp.json()

                if(values['code'] == '1'):
                    invoice.fiscal_signature = values['qrcode']
                    invoice.fiscal_date = datetime.datetime.now()

                    invoice.device_id = values['device_id']
                    invoice.fiscalday = values['FiscalDay']
                    invoice.rgn = values['rgn']
                    invoice.receiptnumber = values['receiptnumbers']
                    invoice.VerificationCode = values['VerificationCode']
                    invoice.bp_number = "200011902"
                    invoice.vat = "10003809"


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
                    message = f"Failed to fiscalize: {values['message']}"

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



# class respartner(models.Model):
#     _inherit = 'res.partner'
    
#     vs = fields.Char(string='TIN Number')
