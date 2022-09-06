odoo.define('point_of_sale.customSaleDetailsButton', function(require) {
    'use strict';

    const Registries = require('point_of_sale.Registries');
    const { Printer } = require('point_of_sale.Printer');
    const SaleDetailsButton = require('point_of_sale.SaleDetailsButton');

    const customSaleDetailsButton = (SaleDetailsButton) => {
        class customSaleDetailsButton extends SaleDetailsButton {

            async onClick() {
            // IMPROVEMENT: Perhaps put this logic in a parent component
            // so that for unit testing, we can check if this simple
            // component correctly triggers an event.
            const saleDetails = await this.rpc({
                model: 'report.point_of_sale.report_saledetails',
                method: 'get_sale_details',
                args: [false, false, false, [this.env.pos.pos_session.id]],
            });
            const report = this.env.qweb.renderToString(
                'SaleDetailsReport',
                Object.assign({}, saleDetails, {
                    date: new Date().toLocaleString(),
                    pos: this.env.pos,
                })
            );
            if (this.env.pos.config.pos_bluetooth_printer) {
                    const printer = new Printer(null, this.env.pos);
                    var xhttp = new XMLHttpRequest();
                    const ticketImage = await printer.htmlToImg(report);
                    xhttp.open("POST", "http://localhost:9100", true);
                    var receiptObj = { image: ticketImage, text: "", copies: 1 };
                    var receiptJSON = JSON.stringify(receiptObj);
                    xhttp.send(receiptJSON);
                }else {
                        const printResult = await this.env.pos.proxy.printer.print_receipt(report);
                        if (!printResult.successful) {
                            await this.showPopup('ErrorPopup', {
                                title: printResult.message.title,
                                body: printResult.message.body,
                            });
                        }
                }
        }

        }
        return customSaleDetailsButton;
    };
    Registries.Component.extend(SaleDetailsButton, customSaleDetailsButton);

});
