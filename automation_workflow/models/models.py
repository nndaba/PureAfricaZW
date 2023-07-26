from lxml import etree
from odoo import models, fields, api, _
import random
import string
import logging 

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_import = fields.Boolean(default=False)
    
    
    def view_sale_receipt(self):
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

    def view_sale_invoice_action(self):
        _logger.info(self.name)
        if self.is_import:
            action = {
                'name': _('Invoices'),
                'domain': [
                    ('invoice_origin', '=', self.name),
                    ('state', '!=', 'cancel'),
                ],
                'view_type': 'form',
                'res_model': 'account.move',
                'view_id': False,
                'view_mode': 'tree,form',
                'type': 'ir.actions.act_window',
            }
            _logger.info(action)

            return action

    @api.model
    def create(self, vals):
        
        # Set the date_order from the sheet if is_import is True
        if vals.get('is_import'):
            
            order_lines = vals.get('order_line')
                        
            for line_command, line_id, line_vals in order_lines:
                if line_vals.get('product_uom_qty'):
                    line_vals['qty_delivered'] = line_vals['product_uom_qty']
                    line_vals['qty_invoiced'] = line_vals['product_uom_qty']

            order = super(SaleOrder, self).create(vals)
            order.write({
                'state':'sale',
                'validity_date': vals.get('date_order')
                })
            
            picking = self.env['stock.picking'].create_stock_picking(order)
            invoice = self.env['account.move']._create_invoice_(order)
            
            _logger.info(34*'&') 
            _logger.info(f"picking = {picking}")
            _logger.info(f"invoice = {invoice}")
            _logger.info(34*'&')

        else:
            order = super(SaleOrder, self).create(vals)
            
                       
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

    def view_invoice_action(self):
        _logger.info(self.name)
        if self.is_import:
            action = {
                'name': _('Invoices'),
                'domain': [
                    ('invoice_origin', '=', self.name),
                    ('state', '!=', 'cancel'),
                ],
                'view_type': 'form',
                'res_model': 'account.move',
                'view_id': False,
                'view_mode': 'tree,form',
                'type': 'ir.actions.act_window',
            }
            _logger.info(action)

            return action

            
    @api.model
    def create(self, vals):
        try:
            if vals.get('is_import'):
                date_order = vals.get('date_order')
                vals['date_order'] = date_order
                
                order_lines = vals.get('order_line')
                            
                for line_command, line_id, line_vals in order_lines:
                    if line_vals.get('product_qty'):
                        line_vals['qty_received'] = line_vals['product_qty']
                        line_vals['qty_invoiced'] = line_vals['product_qty']   #n/i
                
                order = super(PurchaseOrder, self).create(vals)
                
                for line in order.order_line:
                    line.write({
                        'qty_invoiced': line.product_qty,
                    })
                    _logger.info(34*'$')
                    _logger.info(f"Writing to order line {line.id}: {line_vals}")
                    _logger.info(34*'$')
                    line.write(line_vals)
                
                order.write({
                    'state':'purchase',
                    'date_approve': date_order
                    })

                self.env['stock.picking'].create_stock_picking(order)
                self.env['account.move']._create_invoice_(order)
                _logger.info(34*'$')
                _logger.info("Completed all steps")
                _logger.info(34*'$')

            else:
                order = super(PurchaseOrder, self).create(vals)

            return order
        except Exception as e:
            # Handle the exception here or log it
            _logger.error(f"An error occurred during create(): {str(e)}")
            # Create PO with the original vals only (remove is_import flag to avoid recursion)
            order = super(PurchaseOrder, self).create({key: val for key, val in vals.items() if key != 'is_import'})
            return order


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.model
    def create_stock_picking(self, order):
        StockMove = self.env['stock.move']
        subtype_id = self.env['mail.message.subtype'].search([('name', '=', 'Note')], limit=1).id     
        model = ''
        
        if isinstance(order,PurchaseOrder):
       
            picking_type_id = order.picking_type_id
            location_id  = order.picking_type_id.default_location_dest_id.location_id
            location_dest_id = order.picking_type_id.default_location_dest_id
            model = 'purchase.order'

            picking_vals = {
                'partner_id': order.partner_id.id,
                'location_dest_id': order.partner_id.property_stock_supplier.id,
                'location_id': location_id.id,
                'picking_type_id': picking_type_id.id,
                'scheduled_date': order.date_order,
                'date_done' : order.date_order,
                'date_deadline': order.date_order,
                'origin': order.name
            }
            
            picking = self.create(picking_vals)
            
            for line in order.order_line:
                move_vals = {
                    'name': line.product_id.name,
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.product_qty,
                    'quantity_done' : line.product_qty,
                    'picking_id': picking.id,
                    'location_id': line.product_id.property_stock_inventory.location_id.id,
                    'location_dest_id': location_dest_id.id
                
                }
                StockMove.create(move_vals)
            
        elif isinstance(order, SaleOrder):
            model = 'sale.order'
            if order.company_id.id == 1:
                picking_type_id =  self.env['stock.picking.type'].search([('barcode', '=', 'ALL-DELIVERY')], limit=1).id
            else:
                picking_type_id =  self.env['stock.picking.type'].search([('barcode', '=', 'PURE-DELIVERY')], limit=1).id
           
            picking_vals = {
                'partner_id': order.partner_id.id,
                'location_dest_id': order.partner_id.property_stock_customer.id,
                'location_id': order.warehouse_id.lot_stock_id.id,
                'picking_type_id': picking_type_id,
                'scheduled_date': order.date_order,
                'date_done': order.date_order,
                'date_deadline': order.date_order,
                'origin': order.name
            }

            
            _logger.info(34*'$')
            _logger.info(picking_vals)
            _logger.info(34*'$')
            
            picking = self.create(picking_vals)

            for line in order.order_line:
                move_vals = {
                    'name': line.product_id.name,
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.product_uom_qty,
                    'quantity_done' : line.product_uom_qty,
                    'picking_id': picking.id,
                    'location_id': line.product_id.property_stock_inventory.location_id.id,
                    'location_dest_id': order.partner_id.property_stock_customer.id,
                                
                }
                StockMove.create(move_vals)
        else:
            pass

        picking.write({'state':'done'})  # Set the state to 'assigned'

        utilities = self.env['automation.workflow.utilities']
        note = utilities.create_order_note(order,model)

        picking.message_post(body=note)
  
        return True


class AccountMove(models.Model):
    _inherit = 'account.move'

    def _create_invoice_(self, order):
        invoice_line_vals = []
        model = ''
        
        if isinstance(order,PurchaseOrder):
            model = 'purchase.order'
            for line in order.order_line:
                invoice_line_vals.append((0, 0, {
                    'product_id': line.product_id.id,
                    'quantity': line.product_qty,
                    'price_unit': line.price_unit
                }))

            invoice_vals = {
                'move_type': 'in_invoice',
                'partner_id': order.partner_id.id,
                'invoice_date': order.date_order,
                'invoice_date_due': order.date_order,
                'company_id': order.company_id.id,
                'currency_id': order.currency_id.id,
                'invoice_origin': order.name,
                'invoice_line_ids': invoice_line_vals,
                'ref' : order.partner_ref
            }
        elif isinstance(order,SaleOrder):
            model = 'sale.order'
            for line in order.order_line:
                invoice_line_vals.append((0, 0, {
                    'product_id': line.product_id.id,
                    'quantity': line.product_uom_qty,
                    'price_unit': line.price_unit
                }))
                
            invoice_vals = {
                'move_type': 'out_invoice',
                'partner_id': order.partner_id.id,
                'invoice_date': order.date_order,
                'invoice_date_due': order.date_order,
                'company_id': order.company_id.id,
                'currency_id': order.currency_id.id,
                'invoice_origin': order.name,
                'invoice_line_ids': invoice_line_vals,
                'ref': order.client_order_ref
                
            }
            
        else:
            pass
        
        _logger.info(45*'6')
        _logger.info(f"invoice_vals = {invoice_vals}")
        _logger.info(45*'6')
        
        invoice = self.env['account.move'].sudo().create(invoice_vals)
        
        _logger.info(45*'@')
        _logger.info(f"invoice = {invoice}")
        _logger.info(45*'@')

        invoice.write({'state': 'posted'})

        utilities = self.env['automation.workflow.utilities']
        note = utilities.create_order_note(order, model)

        invoice.message_post(body=note)

        return invoice
    
    
class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    qty_invoiced = fields.Float(compute='_compute_qty_invoiced', string="Billed Qty", digits='Product Unit of Measure', store=True)

    @api.depends('invoice_lines.move_id.state', 'invoice_lines.quantity', 'qty_received', 'product_uom_qty', 'order_id.state', 'order_id.is_import')
    def _compute_qty_invoiced(self):
        for line in self:
            if line.order_id.is_import:
                # If is_import in purchase order is True, set qty_invoiced to product_qty
                line.qty_invoiced = line.product_qty
            else:
                # Otherwise, apply the original computation logic
                qty = 0.0
                for inv_line in line._get_invoice_lines():
                    if inv_line.move_id.state not in ['cancel'] or inv_line.move_id.payment_state == 'invoicing_legacy':
                        if inv_line.move_id.move_type == 'in_invoice':
                            qty += inv_line.product_uom_id._compute_quantity(inv_line.quantity, line.product_uom)
                        elif inv_line.move_id.move_type == 'in_refund':
                            qty -= inv_line.product_uom_id._compute_quantity(inv_line.quantity, line.product_uom)
                line.qty_invoiced = qty


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    # Analytic & Invoicing fields
    qty_invoiced = fields.Float(
        string="Invoiced Quantity",
        compute='_compute_qty_invoiced',
        digits='Product Unit of Measure',
        store=True)
    
    @api.depends('invoice_lines.move_id.state', 'invoice_lines.quantity')
    def _compute_qty_invoiced(self):
        """
        Compute the quantity invoiced. If case of a refund, the quantity invoiced is decreased. Note
        that this is the case only if the refund is generated from the SO and that is intentional: if
        a refund made would automatically decrease the invoiced quantity, then there is a risk of reinvoicing
        it automatically, which may not be wanted at all. That's why the refund has to be created from the SO
        """
    
        for line in self:
            if line.order_id.is_import:
                # If is_import in sale order is True, set qty_invoiced to product_qty
                line.qty_invoiced = line.product_uom_qty
            else:
                qty_invoiced = 0.0
                for invoice_line in line._get_invoice_lines():
                    if invoice_line.move_id.state != 'cancel' or invoice_line.move_id.payment_state == 'invoicing_legacy':
                        if invoice_line.move_id.move_type == 'out_invoice':
                            qty_invoiced += invoice_line.product_uom_id._compute_quantity(invoice_line.quantity, line.product_uom)
                        elif invoice_line.move_id.move_type == 'out_refund':
                            qty_invoiced -= invoice_line.product_uom_id._compute_quantity(invoice_line.quantity, line.product_uom)
                line.qty_invoiced = qty_invoiced
    
               
            
class Utilities(models.AbstractModel):
    _name = 'automation.workflow.utilities'

    def get_order_url(self, order_id, model):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        order = self.env[model].search([('id', '=', order_id)], limit=1)

        order_url = f"{base_url}/web#id={order.id}&model={model}&view_type=form"

        return order_url

    def create_order_note(self, order, model):
        order_url = self.get_order_url(order.id, model)

        note = "This transfer has been created from: <a href='{}'>{}</a>".format(
            order_url,
            order.name
        )
        return note

