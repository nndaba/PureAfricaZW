odoo.define('pos_bluetooth_printer.LabelReceipt', function(require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const Registries = require('point_of_sale.Registries');
    const { onWillUpdateProps } = owl;

    class LabelReceipt extends PosComponent {
        setup() {
            super.setup();
            this._receiptEnv = this.props.order.getOrderReceiptEnv();
            onWillUpdateProps((nextProps) => {
                this._receiptEnv = nextProps.order.getOrderReceiptEnv();
            });
        }
        willUpdateProps(nextProps) {
            this._receiptEnv = nextProps.order.getOrderReceiptEnv();
        }
        get receipt() {
            return this.receiptEnv.receipt;
        }
        get orderlines() {
            return this.receiptEnv.orderlines;
        }

        get compute_product(){
            var order_lines = this.receipt.orderlines
            var product = {
                'orderlines': [],
                'orderlines_q': []
            }
            for (var i = 0; i <= order_lines.length - 1; i++){
                if(!product.orderlines.includes(order_lines[i])){
                    product.orderlines.push(order_lines[i]);
                    product.orderlines_q.push({
                        id: order_lines[i].id,
                        category: order_lines[i].pos_categ_id[0],
                        categoryName: order_lines[i].pos_categ_id[1],
                        quantity: order_lines[i].quantity,
                        quantity_q: this.get_quantity(order_lines[i].quantity)
                    });
                }
            }
            return product;

        }
        get_quantity(quantity) {
            var new_quantity = [];
            var i = 0
            while ( i < quantity) {
                new_quantity.push(i);
                i++;
            }

            return new_quantity;
        }

        get paymentlines() {
            return this.receiptEnv.paymentlines;
        }
        get isTaxIncluded() {
            return Math.abs(this.receipt.subtotal - this.receipt.total_with_tax) <= 0.000001;
        }
        get receiptEnv () {
          return this._receiptEnv;
        }
        isSimple(line) {
            return (
                line.discount === 0 &&
                line.is_in_unit &&
                line.quantity === 1 &&
                !(
                    line.display_discount_policy == 'without_discount' &&
                    line.price < line.price_lst
                )
            );
        }
    }
    LabelReceipt.template = 'LabelReceipt';

    Registries.Component.add(LabelReceipt);


    return LabelReceipt;
});
