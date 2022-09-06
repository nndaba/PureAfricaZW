odoo.define('BluetoothPrinterReceiptScreen', function (require) {
    "use strict";

    const {Printer} = require('point_of_sale.Printer');
    const Registries = require('point_of_sale.Registries');
    const ReceiptScreen = require('point_of_sale.ReceiptScreen');

    const customReceiptScreen = ReceiptScreen => {
        class customReceiptScreen extends ReceiptScreen {

            constructor() {
                super(...arguments);
                var order = this.env.pos.get_order();
            }

            get currentOrder() {
                return this.env.pos.get_order();
            }

            get_is_openCashDrawer() {
                return this.currentOrder.is_paid_with_cash() || this.currentOrder.get_change();
            }

            get compute_product() {
                var add = [];
                var product = this.currentOrder.get_orderlines();
                if (product.length > 0) {
                    if (this.env.pos.config.receipt_types_views === "labelReceipt") {
                        for (var n = 0; n < product.length; n++) {
                            for (var nq = 0; nq < product[n].quantity; nq++) {
                                add.push(product[n])
                            }
                        }
                    }
                }
                return {
                    'products': add,

                };
            }

            async handleAutoPrint() {
                if (this._shouldAutoPrint()) {
                    if (this.env.pos.config.bluetooth_print_auto) {
                        await this.printReceiptAndLabel();
                        if (this.currentOrder._printed && this._shouldCloseImmediately()) {
                            this.whenClosing();
                         }
                    }else {
                        await this.printReceipt();
                        if (this.currentOrder._printed && this._shouldCloseImmediately()) {
                            this.whenClosing();
                        }
                    }

                }
            }

            async printReceiptAndLabel() {
                if (this.env.pos.config.pos_bluetooth_printer) {
                    const printer = new Printer(null, this.env.pos);
                    var xhttp = new XMLHttpRequest();
                    const timer = ms => new Promise(res => setTimeout(res, ms))
                    for (var i = 0; i < $(".pos-receipt").length; i++) {
                        const receiptString = $(".pos-receipt")[i].outerHTML;
                        const ticketImage = await printer.htmlToImg(receiptString);
                        const copie = this.env.pos.config.receipt_copies;
                        if (i === 0) {
                            xhttp.open("POST", "http://localhost:9100", true);
                            var receiptObj = {
                                image: ticketImage,
                                text: "",
                                "openCashDrawer": !!this.get_is_openCashDrawer(),
                                copies: copie
                            };
                        } else if (i !== 0) {
                            if (!this.env.pos.config.is_different_printer) {
                                xhttp.open("POST", "http://localhost:9100", true);
                            } else {
                                xhttp.open("POST", "http://localhost:9200", true);
                            }
                            var receiptObj = {image: ticketImage, text: "", copies: 1};
                        }
                        var receiptJSON = JSON.stringify(receiptObj);
                        xhttp.send(receiptJSON);
                        await timer(1000);

                    }

                }

            }

            async printReceipt() {
                if (this.env.pos.config.pos_bluetooth_printer) {
                    const printer = new Printer(null, this.env.pos);
                    var xhttp = new XMLHttpRequest();
                    const receiptString = this.orderReceipt.comp.el.outerHTML;
                    const ticketImage = await printer.htmlToImg(receiptString);
                    const copie = this.env.pos.config.receipt_copies;
                    xhttp.open("POST", "http://localhost:9100", true);
                    var receiptObj = { image: ticketImage, text: "","openCashDrawer":!!this.get_is_openCashDrawer(), copies: copie };
                    var receiptJSON = JSON.stringify(receiptObj);
                    xhttp.send(receiptJSON);
                }else{
                    const isPrinted = await this._printReceipt();
                     if (isPrinted) {
                    this.currentOrder._printed = true;
                    }
                }
            }

            async printLabel() {
                if (this.env.pos.config.pos_bluetooth_printer) {
                    const printer = new Printer(null, this.env.pos);
                    var xhttp = new XMLHttpRequest();
                    let i = 1;
                    const timer = ms => new Promise(res => setTimeout(res, ms))
                    while (i < $(".pos-receipt").length) {
                        const receiptString = $(".pos-receipt")[i].outerHTML;
                        const ticketImage = await printer.htmlToImg(receiptString);
                        const copie = this.env.pos.config.receipt_copies;
                        if (!this.env.pos.config.is_different_printer) {
                            xhttp.open("POST", "http://localhost:9100", true);
                        } else {
                            xhttp.open("POST", "http://localhost:9200", true);
                        }
                        var receiptObj = {image: ticketImage, text: "", copies: 1};
                        var receiptJSON = JSON.stringify(receiptObj);
                        xhttp.send(receiptJSON);
                        i++;
                        await timer(1000);
                    }

                }

            }


        }

        return customReceiptScreen;
    };


    Registries.Component.extend(ReceiptScreen, customReceiptScreen);

});

