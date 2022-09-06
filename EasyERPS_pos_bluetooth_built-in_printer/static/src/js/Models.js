odoo.define('pos_bluetooth_printer.Models', function (require) {
"use strict";

var models = require('point_of_sale.models');
var core = require('web.core');
var _t = core._t;
var { Gui } = require('point_of_sale.Gui');

models.load_fields('product.product','pos_categ_id');

models.load_models([{
    model: 'pos.category',
    condition: function(self){ return self.config.receipt_types_views === "categoryReceipt"; },
    fields: ['name'],
    loaded: function(self,category){
        if(category.length){
            self.pos_categ_id = [];
            for(var i=0;i<category.length;i++){
                self.pos_categ_id.push(category[i].id)
            }
        } else {
                 Gui.showPopup('ErrorPopup', {
                    title: _t('No PoS Product Categories Found'),
                    body: _t('Please add PoS Product Categories to print Categories Receipt.'),
                });
            }
    },
    }],{'after': 'product.product'});

    var _super_orderLine = models.Orderline.prototype;
    models.Orderline = models.Orderline.extend({
        export_for_printing: function(){
            var result = _super_orderLine.export_for_printing.apply(this, arguments);
            result.pos_categ_id = this.get_product().pos_categ_id;
            return result;
        }
    });

    var _super_order = models.Order.prototype;
    models.Order = models.Order.extend({
        export_for_printing: function() {
            var result = _super_order.export_for_printing.apply(this,arguments);
            var date    = new Date();
            result.date.LocaleStringdateStyle = date.toLocaleString('en-US', {day: "2-digit"})+" "+ date.toLocaleString('en-US', { month: "short"})+" "+date.toLocaleString('en-US', { year: "numeric"});
            result.date.LocaleStringtimeStyle = date.toLocaleString('en-US', { timeStyle: "short" ,hour12: true });
            return result;
        },
    });

});

