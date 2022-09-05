odoo.define('point_of_sale.customPaymentScreen', function (require) {
    'use strict';
    const { Printer } = require('point_of_sale.Printer');
    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const Registries = require('point_of_sale.Registries');


    const customPaymentScreen = (PaymentScreen) => {
        class customPaymentScreen extends PaymentScreen {

            bluetoothOenCashbox() {
                if (this.env.pos.config.pos_bluetooth_printer) {
                        const printer = new Printer(null, this.env.pos);
                        var xhttp = new XMLHttpRequest();
                            xhttp.open("POST", "http://localhost:9100", true);
                            var receiptObj = {"openCashDrawer":true};
                            var receiptJSON = JSON.stringify(receiptObj);
                            xhttp.send(receiptJSON);
                    }else{
                        this.env.pos.proxy.printer.open_cashbox();
                        }
            }


        }
        return customPaymentScreen;
    };
    Registries.Component.extend(PaymentScreen, customPaymentScreen);

});
