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
    receipt_count = fields.Integer(compute='_compute_receipt_count', string='Receipt Count')

    def receipt_count(self):
        self.receipt_count = 1
        # for order in self:
            # order.receipt_count = self.env['stock.picking'].search_count([('purchase_id', '=', order.id)])


    def view_receipt(self):
        _logger.info(self.name)
        if self.is_import:
            action = {
                'name': _('Receipts'),
                'domain': [
                    ('origin', '=', self.name),
                    ('state', '!=', 'cancel'),
                ],
                'view_type': 'form',
                'res_model': 'stock.picking',
                'view_id': False,
                'view_mode': 'tree,form',
                'type': 'ir.actions.act_window',
            }
            _logger.info(action)

            return action

            
    @api.model
    def create(self, vals):
        if vals.get('is_import'):
            date_order = vals.get('date_order')
            vals['date_order'] = date_order
          

            order = super(PurchaseOrder, self).create(vals)

            order.write({
                'state':'purchase',
                'date_approve': date_order
                })

            self.env['stock.picking'].create_stock_picking(order)

        else:
            order = super(PurchaseOrder, self).create(vals)

        return order


class StockPicking(models.Model):
    _inherit = 'stock.picking'

 

    @api.model
    def create_stock_picking(self, order):
        StockMove = self.env['stock.move']
        subtype_id = self.env['mail.message.subtype'].search([('name', '=', 'Note')], limit=1).id
       
        picking_type_id = order.picking_type_id
        location_id  = order.picking_type_id.default_location_dest_id.location_id
        location_dest_id = order.picking_type_id.default_location_dest_id

        picking_vals = {
            'partner_id': order.partner_id.id,
            'location_dest_id': order.partner_id.property_stock_supplier.id,
            'location_id': location_id.id,
            'picking_type_id': picking_type_id.id,
            'scheduled_date': order.date_order,
            'date_deadline': order.date_order,
            'origin': order.name
        }
        picking = self.create(picking_vals)

        purchase_order_url = self.get_purchase_order_url(order.id)

        note = "This transfer has been created from: <a href='{}'>{}</a> ({})".format(
            purchase_order_url,
            order.name,
            order.partner_ref
        )
        picking.message_post(body=note)

        for line in order.order_line:
            move_vals = {
                'name': line.product_id.name,
                'product_id': line.product_id.id,
                'product_uom_qty': line.product_qty,
                'picking_id': picking.id,
                'location_id': line.product_id.property_stock_inventory.location_id.id,
                'location_dest_id': location_dest_id.id
            
            }
            StockMove.create(move_vals)

       

        return True


    def get_purchase_order_url(self, order_id):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        order = self.env['purchase.order'].search([('id', '=', order_id)], limit=1)

        model = 'purchase.order'
        purchase_order_url = f"{base_url}/web#id={order.id}&model={model}&view_type=form"

        return purchase_order_url
