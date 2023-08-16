from lxml import etree
from odoo import models, fields, api, _
import random
import string
import logging 
_logger = logging.getLogger(__name__)


    
class PurchaseOrderPickWizard(models.TransientModel):
    _name = 'purchase.wizard'
    _description = 'Purchase Order Pick Wizard'

    order_ids = fields.Many2many('purchase.order', string='Selected Orders')
    
    @api.model
    def default_get(self, fields):
        res = super(PurchaseOrderPickWizard, self).default_get(fields)
        selected_orders = self._context.get('active_ids', [])
        res['order_ids'] = [(6, 0, selected_orders)]
        return res
    
    def action_execute(self):
        for order in self.order_ids:
            if order.state == 'draft':
                original_date_order = order.date_order
                order.button_confirm()
                order.write({'date_approve': original_date_order})
                
                # Execute action_set_quantities_to_reservation on stock.picking
                if order.picking_ids:
                    for picking in order.picking_ids:
                        picking.action_set_quantities_to_reservation()

                        # Call button_validate on stock.picking
                        picking.button_validate()
                        
                        
                 # Create the vendor bill
                self.env['purchase.order'].sudo().browse(order.id).action_create_invoice()
            
            
                # Set the invoice date for the vendor bill
                if order.invoice_ids:
                    for invoice in order.invoice_ids:
                        invoice.write({
                            'invoice_date': original_date_order,
                            'date': original_date_order,
                            'invoice_date_due':original_date_order
                            })

                        # Post the vendor bill
                        self.env['account.move'].sudo().browse(invoice.id).action_post()
                        
        return True
                
                    
                
 
    
class SaleOrderPickWizard(models.TransientModel):
    _name = 'sale.wizard'
    _description = 'Sale Order Pick Wizard'

    order_ids = fields.Many2many('sale.order', string='Selected Orders')
    
    @api.model
    def default_get(self, fields):
        res = super(SaleOrderPickWizard, self).default_get(fields)
        selected_orders = self._context.get('active_ids', [])
        res['order_ids'] = [(6, 0, selected_orders)]
        return res

    def action_execute(self):
        # Logic to perform the desired action on the selected orders
        for order in self.order_ids:
            if order.state == 'draft':
                # Confirm the order
                original_date_order = order.date_order
                order.action_confirm()
            
                # Check if the order has a picking and the picking's products_availability is not 'available'
                if order.picking_ids and order.picking_ids.filtered(lambda picking: picking.products_availability != 'Available'):
                    _logger.info("Not Available")
                    _logger.info("Not Available")
                    # Cancel the order
                    order.write({'state':'draft'})
                    
                    # Delete the stock picking
                    order.picking_ids.action_cancel()
                    order.picking_ids.unlink()
                    order.date_order = original_date_order
                else:
                    _logger.info("Available")
                    _logger.info("Available")
                    order.write({'date_order': original_date_order})
            
                    #Execute action_set_quantities_to_reservation on stock.pickings
                    if order.picking_ids:
                        self.env['sale.order'].sudo().browse(order.id).action_view_delivery()
                        
                        for picking in order.picking_ids:
                            self.env['stock.picking'].sudo().browse(picking.id).action_set_quantities_to_reservation()
                            
                            picking.scheduled_date = original_date_order
                            picking.date_done = original_date_order
                            
                            # Validate the stock picking
                            self.env['stock.picking'].sudo().browse(picking.id).button_validate()
                            picking.write({'date_done':original_date_order})
                            
                    
            
                    # Invoke the "Create Invoice" action on sale.order
                    invoice = self.env['sale.advance.payment.inv'].with_context({
                        'active_model': 'sale.order',
                        'active_id': order.id,
                    }).create({
                        'advance_payment_method': 'delivered',
                    })._create_invoices(order)
                        
            
                    if invoice:
                        invoice.invoice_date = original_date_order
                        invoice.action_post()
                    
        return True
            
            