from odoo import models, fields, api, _
import random
import string
import logging 

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_import = fields.Boolean(default=False)

    @api.model
    def create(self, vals):
        # Set the date_order from the sheet if is_import is True
        if vals.get('is_import'):
            validity_date = vals.get('date_order')

        order = super(SaleOrder, self).create(vals)

        # Perform action_confirm if is_import is True
        if vals.get('is_import'):
            order.action_confirm()

            #Execute action_set_quantities_to_reservation on stock.pickings
            if order.picking_ids:
                self.env['sale.order'].sudo().browse(order.id).action_view_delivery()



                for picking in order.picking_ids:

                    if picking.state not in ['assigned']:

                        self.env['stock.picking'].sudo().browse(picking.id).action_set_quantities_to_reservation()
                        
                        # Validate the stock picking
                        self.env['stock.picking'].sudo().browse(picking.id).button_validate()

            # Invoke the "Create Invoice" action on sale.order
            invoice = self.env['sale.advance.payment.inv'].with_context({
                'active_model': 'sale.order',
                'active_id': order.id,
            }).create({
                'advance_payment_method': 'delivered',
            })._create_invoices(order)


            if invoice:
                invoice.invoice_date = order.date_order
                invoice.action_post()
        
        return order

    
class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    is_import = fields.Boolean(default=False)

    @api.model
    def create(self, vals):
        # Set the date_order from the sheet if is_import is True
        if vals.get('is_import'):
            date_order = vals.get('date_order')

        order = super(PurchaseOrder, self).create(vals)

        # Perform button_confirm action if is_import is True
        if vals.get('is_import'):
            order.button_confirm()

            # Execute action_set_quantities_to_reservation on stock.picking
#             _logger.info(order.picking_ids)
#             if order.picking_ids:
#                 _logger.info(order.picking_ids)
#                 for picking in order.picking_ids:
#                     _logger.info(picking)
#                     picking.action_set_quantities_to_reservation()

#                     # Call button_validate on stock.picking
#                     picking.button_validate()


#              # Create the vendor bill
#             self.env['purchase.order'].sudo().browse(order.id).action_create_invoice()

#             # Set the invoice date for the vendor bill
#             if order.invoice_ids:
#                 for invoice in order.invoice_ids:
#                     invoice.write({
#                         'invoice_date': order.date_order,
#                         'date': order.date_order,
#                         'invoice_date_due':order.date_order
#                         })

#                     # Post the vendor bill
#                     self.env['account.move'].sudo().browse(invoice.id).action_post()
            
        return order


