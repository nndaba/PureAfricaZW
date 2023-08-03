// BiProductScreen js
odoo.define('bi_pos_stock.productScreen', function(require) {
	"use strict";

	const Registries = require('point_of_sale.Registries');
	const ProductScreen = require('point_of_sale.ProductScreen');

	const BiProductScreen = (ProductScreen) =>
		class extends ProductScreen {
			setup() {
            	super.setup();
            }

			async _clickProduct(event) {
				let self = this;
				const product = event.detail;
				let allow_order = self.env.pos.config.pos_allow_order;
				let pos_config = self.env.pos.config;
				let deny_order= self.env.pos.config.pos_deny_order || 0;
				let call_super = true;
				if(self.env.pos.config.pos_display_stock && product.type == 'product'){
					if (allow_order == false){
						if (pos_config.pos_stock_type == 'onhand'){
							if ( product.bi_on_hand <= 0 ){
								call_super = false;
								self.showPopup('ErrorPopup', {
									title: self.env._t('Deny Order'),
									body: self.env._t("Deny Order" + "(" + product.display_name + ")" + " is Out of Stock."),
								});
							}
						}
						if (pos_config.pos_stock_type == 'incoming'){
							if ( product.incoming_qty <= 0 ){
								call_super = false;
								self.showPopup('ErrorPopup', {
									title: self.env._t('Deny Order'),
									body: self.env._t("Deny Order" + "(" + product.display_name + ")" + " is Out of Stock."),
								});
							}
						}
						if (pos_config.pos_stock_type == 'outgoing'){
							if ( product.outgoing_qty <= 0 ){
								call_super = false;
								self.showPopup('ErrorPopup', {
									title: self.env._t('Deny Order'),
									body: self.env._t("Deny Order" + "(" + product.display_name + ")" + " is Out of Stock."),
								});
							}
						}
						if (pos_config.pos_stock_type == 'available'){
							if ( product.bi_available <= 0 ){
								call_super = false;
								self.showPopup('ErrorPopup', {
									title: self.env._t('Deny Order'),
									body: self.env._t("Deny Order" + "(" + product.display_name + ")" + " is Out of Stock."),
								});
							}
						}
					}else{
						if (pos_config.pos_stock_type == 'onhand'){
							if ( product.bi_on_hand <= deny_order ){
								call_super = false;
								self.showPopup('ErrorPopup', {
									title: self.env._t('Deny Order'),
									body: self.env._t("Deny Order" + "(" + product.display_name + ")" + " is Out of Stock."),
								});
							}
						}
						if (pos_config.pos_stock_type == 'incoming'){
							if ( product.incoming_qty <= deny_order ){
								call_super = false;
								self.showPopup('ErrorPopup', {
									title: self.env._t('Deny Order'),
									body: self.env._t("Deny Order" + "(" + product.display_name + ")" + " is Out of Stock."),
								});
							}
						}
						if (pos_config.pos_stock_type == 'outgoing'){
							if ( product.outgoing_qty <= deny_order ){
								call_super = false;
								self.showPopup('ErrorPopup', {
									title: self.env._t('Deny Order'),
									body: self.env._t("Deny Order" + "(" + product.display_name + ")" + " is Out of Stock."),
								});
							}
						}
						if (pos_config.pos_stock_type == 'available'){
							if ( product.bi_available <= deny_order ){
								call_super = false;
								self.showPopup('ErrorPopup', {
									title: self.env._t('Deny Order'),
									body: self.env._t("Deny Order" + "(" + product.display_name + ")" + " is Out of Stock."),
								});
							}
						}
					}
				}
				if(call_super){
					super._clickProduct(event);
				}
			}

			async _onClickPay() {
				var self = this;
				let order = this.env.pos.get_order();
				let lines = order.get_orderlines();
				let pos_config = self.env.pos.config;
				let allow_order = pos_config.pos_allow_order;
				let deny_order= pos_config.pos_deny_order || 0;
				let call_super = true;
				if(pos_config.pos_display_stock){
					let prod_used_qty = {};
					$.each(lines, function( i, line ){
						let prd = line.product;
						if (prd.type == 'product'){
							if(pos_config.pos_stock_type == 'onhand'){
								if(prd.id in prod_used_qty){
									let old_qty = prod_used_qty[prd.id][1];
									prod_used_qty[prd.id] = [prd.bi_on_hand,line.quantity+old_qty]
								}else{
									prod_used_qty[prd.id] = [prd.bi_on_hand,line.quantity]
								}
							}
							if(pos_config.pos_stock_type == 'incoming'){
								if(prd.id in prod_used_qty){
									let old_qty = prod_used_qty[prd.id][1];
									prod_used_qty[prd.id] = [prd.incoming_qty,line.quantity+old_qty]
								}else{
									prod_used_qty[prd.id] = [prd.incoming_qty,line.quantity]
								}	
							}
							if(pos_config.pos_stock_type == 'outgoing'){

								if(prd.id in prod_used_qty){
									let old_qty = prod_used_qty[prd.id][1];
									prod_used_qty[prd.id] = [prd.outgoing_qty,line.quantity]
								}else{
									prod_used_qty[prd.id] = [prd.outgoing_qty,line.quantity]
								}	
							}
							if(pos_config.pos_stock_type == 'available'){
								if(prd.id in prod_used_qty){
									let old_qty = prod_used_qty[prd.id][1];
									prod_used_qty[prd.id] = [prd.bi_available,line.quantity+old_qty]
								}else{
									prod_used_qty[prd.id] = [prd.bi_available,line.quantity]
								}
							}

							
						}
					});

					$.each(prod_used_qty, function( i, pq ){
						let product = self.env.pos.db.get_product_by_id(i);
						if (allow_order == false && pq[0] < pq[1]){
							call_super = false;
							self.showPopup('ErrorPopup', {
								title: self.env._t('Deny Order'),
								body: self.env._t("Deny Order" + "(" + product.display_name + ")" + " is Out of Stock."),
							});
						}
						let check = pq[0] - pq[1];
						if (allow_order == true && check < deny_order){
							call_super = false;
							self.showPopup('ErrorPopup', {
								title: self.env._t('Deny Order'),
								body: self.env._t("Deny Order" + "(" + product.display_name + ")" + " is Out of Stock."),
							});
						}
					});
				}
				if(call_super){
					super._onClickPay();
				}
			}
		};

	Registries.Component.extend(ProductScreen, BiProductScreen);

	return ProductScreen;

});
