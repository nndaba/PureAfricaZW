odoo.define('point_of_sale.customReprintReceiptScreen', function (require) {
    'use strict';
    const {Printer} = require('point_of_sale.Printer');
    const ReprintReceiptScreen = require('point_of_sale.ReprintReceiptScreen');
    const Registries = require('point_of_sale.Registries');

    const customReprintReceiptScreen = (ReprintReceiptScreen) => {
        class customReprintReceiptScreen extends ReprintReceiptScreen {

            get compute_product() {
                var add = [];
                var product = this.props.order.get_orderlines();
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

            async printReceiptAndLabel() {
                if (this.env.pos.config.pos_bluetooth_printer) {
                    const printer = new Printer(null, this.env.pos);
                    var xhttp = new XMLHttpRequest();
                    const timer = ms => new Promise(res => setTimeout(res, ms))
                    for (var i = 0; i < $(".pos-receipt").length; i++) {
                        const receiptString = $(".pos-receipt")[i].outerHTML;
                        const ticketImage = await printer.htmlToImg(receiptString);
                        if (i === 0) {
                            xhttp.open("POST", "http://localhost:9100", true);
                            var receiptObj = {image: ticketImage, text: "", copies: 1};
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
                    xhttp.open("POST", "http://localhost:9100", true);
                    var receiptObj = {image: ticketImage, text: "", copies: 1};
                    var receiptJSON = JSON.stringify(receiptObj);
                    xhttp.send(receiptJSON);
                } else if (this.env.pos.proxy.printer && this.env.pos.config.iface_print_skip_screen) {
                    let result = await this._printReceipt();
                    if (result)
                        this.showScreen('TicketScreen', {reuseSavedUIState: true});
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

        return customReprintReceiptScreen;
    };
    Registries.Component.extend(ReprintReceiptScreen, customReprintReceiptScreen);

});
