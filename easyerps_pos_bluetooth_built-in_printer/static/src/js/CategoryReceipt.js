odoo.define('pos_bluetooth_printer.CategoryReceipt', function(require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const Registries = require('point_of_sale.Registries');
    const { onWillUpdateProps } = owl;


    class CategoryReceipt extends PosComponent {
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

        get computeCategory(){
            var order_lines = this.receipt.orderlines;
            var categ = {
                'category': [],
                'categorys': [],
            }
            for (var i = 0; i <= order_lines.length - 1; i++){
                if(!categ.category.includes(order_lines[i].pos_categ_id[0])){
                    categ.category.push(order_lines[i].pos_categ_id[0]);
                    categ.categorys.push({category_id: order_lines[i].pos_categ_id[0],category_name: order_lines[i].pos_categ_id[1]});
                }
            }
            return categ;

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
    CategoryReceipt.template = 'CategoryReceipt';

    Registries.Component.add(CategoryReceipt);


    return CategoryReceipt;
});
