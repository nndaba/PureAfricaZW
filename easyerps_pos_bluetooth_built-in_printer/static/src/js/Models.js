odoo.define('pos_bluetooth_printer.Models', function (require) {
"use strict";

const { PosGlobalState, Order, Orderline, Payment } = require('point_of_sale.models');
const Registries = require('point_of_sale.Registries');
const core = require('web.core');
const QWeb = core.qweb;
var _t = core._t;
var { Gui } = require('point_of_sale.Gui');

const PosBluetoothPosGlobalState = (PosGlobalState) => class PosBluetoothPosGlobalState extends PosGlobalState {

    async _processData(loadedData) {
        await super._processData(...arguments);
        if (this.config.receipt_types_views === "categoryReceipt") {
            this._loadBluetoothcategory(loadedData['pos.category']);
        }
    }
    _loadBluetoothcategory(category) {
        if(category.length){
            this.pos_categ_id = [];
            for(var i=0;i<category.length;i++){
                this.pos_categ_id.push(category[i].id)
            }
        }else {
                 Gui.showPopup('ErrorPopup', {
                    title: _t('No PoS Product Categories Found'),
                    body: _t('Please add PoS Product Categories to print Categories Receipt.'),
                });
            }
    }
}
Registries.Model.extend(PosGlobalState, PosBluetoothPosGlobalState);

const PosBluetoothOrderline = (Orderline) => class PosBluetoothOrderline extends Orderline {
    export_for_printing() {
        const result = super.export_for_printing(...arguments);
        result.pos_categ_id = this.get_product().pos_categ_id;
        return result;
    }

}
Registries.Model.extend(Orderline, PosBluetoothOrderline);

const PosBluetoothOrder = (Order) => class PosRestaurantOrder extends Order {
    export_as_JSON() {
        const json = super.export_as_JSON(...arguments);
        const date = new Date();
        json.LocaleStringdateStyle = date.toLocaleString('en-US', {day: "2-digit"})+" "+ date.toLocaleString('en-US', { month: "short"})+" "+date.toLocaleString('en-US', { year: "numeric"});
        json.LocaleStringtimeStyle = date.toLocaleString('en-US', { timeStyle: "short" ,hour12: true });
        json.sequence_number = this.sequence_number;
        return json;
    }
    export_for_printing() {
        const result = super.export_for_printing(...arguments);
        const date = new Date();
        result.date.LocaleStringdateStyle = date.toLocaleString('en-US', {day: "2-digit"})+" "+ date.toLocaleString('en-US', { month: "short"})+" "+date.toLocaleString('en-US', { year: "numeric"});
        result.date.LocaleStringtimeStyle = date.toLocaleString('en-US', { timeStyle: "short" ,hour12: true });
        return result;
    }
}
Registries.Model.extend(Order, PosBluetoothOrder);


});

