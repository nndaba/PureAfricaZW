// BiProductScreen js
odoo.define('bi_pos_stock.ProductsWidget', function(require) {
	"use strict";

	const ProductsWidget = require('point_of_sale.ProductsWidget');
	const PosComponent = require('point_of_sale.PosComponent');
    const { useListener } = require("@web/core/utils/hooks");
    const Registries = require('point_of_sale.Registries');
    const { onMounted } = owl;
    const {Product} = require('point_of_sale.models');
    const { onWillUnmount, useState } = owl;

	let prd_list_count = 0;

	const BiProductsWidget = (ProductsWidget) =>
		class extends ProductsWidget {
			setup() {
	            super.setup();
	            var self = this;
				onMounted(() => this._mounted());
	        }

			_mounted() {
				var self = this;
				self.env.services['bus_service'].addEventListener('notification', ({ detail: notifications }) => {
					self.syncProdData(notifications);
				});
			}

			syncProdData(notifications){

				let self = this;
				notifications.forEach(function (ntf) {
					ntf = JSON.parse(JSON.stringify(ntf))
					if(ntf && ntf.type && ntf.type == "product.product/sync_data"){
						let prod = ntf.payload.product[0];
						let old_category_id = self.env.pos.db.product_by_id[prod.id];
						let new_category_id = prod.pos_categ_id[0];
						let stored_categories = self.env.pos.db.product_by_category_id;

						prod.pos = self.env.pos;
						if(self.env.pos.db.product_by_id[prod.id]){
							if(old_category_id.pos_categ_id){
								stored_categories[old_category_id.pos_categ_id[0]] = stored_categories[old_category_id.pos_categ_id[0]].filter(function(item) {
									return item != prod.id;
								});
							}
							if(stored_categories[new_category_id]){
								stored_categories[new_category_id].push(prod.id);
							}
							let updated_prod = self.updateProd(prod);
						}else{
							let updated_prod = self.updateProd(prod);
						}
					}
				});
				self.env.pos.is_sync = true;
			}

			updateProd(product){
				let self = this;
				self.env.pos._loadProductProduct([product]);
				const productMap = {};
				const productTemplateMap = {};

				product.pos = self.env.pos; 
				product.applicablePricelistItems = {};
				productMap[product.id] = product;
				productTemplateMap[product.product_tmpl_id[0]] = (productTemplateMap[product.product_tmpl_id[0]] || []).concat(product);
				let new_prod =  Product.create(product);

				for (let pricelist of self.env.pos.pricelists) {
					for (const pricelistItem of pricelist.items) {
						if (pricelistItem.product_id) {
							let product_id = pricelistItem.product_id[0];
							let correspondingProduct = productMap[product_id];
							if (correspondingProduct) {
								self.env.pos._assignApplicableItems(pricelist, correspondingProduct, pricelistItem);
							}
						}
						else if (pricelistItem.product_tmpl_id) {
							let product_tmpl_id = pricelistItem.product_tmpl_id[0];
							let correspondingProducts = productTemplateMap[product_tmpl_id];
							for (let correspondingProduct of (correspondingProducts || [])) {
								self.env.pos._assignApplicableItems(pricelist, correspondingProduct, pricelistItem);
							}
						}
						else {
							self.env.pos._assignApplicableItems(pricelist, product, pricelistItem);
						}
					}
				}
				self.env.pos.db.product_by_id[product.id] = new_prod ;
			}

			get is_sync() {
				return this.env.pos.is_sync;
			}

			willUnmount() {
				super.willUnmount();
				this.env.pos.off('change:is_sync', null, this);
			}

			_switchCategory(event) {
				this.env.pos.synch.is_sync = true
				super._switchCategory(event);
			}

			get productsToDisplay() {
				let self = this;
				let prods = super.productsToDisplay;
				let location = this.env.pos.custom_stock_locations;
				if (self.env.pos.config.show_stock_location == 'specific'){
					if (self.env.pos.config.pos_stock_type == 'onhand'){
						$.each(prods, function( i, prd ){
							prd['bi_on_hand'] = 0;
							let loc_onhand = JSON.parse(prd.quant_text);
							$.each(loc_onhand, function( k, v ){
								if(location[0]['id'] == parseInt(k)){
									prd['bi_on_hand'] = v[0];
								}
							})
						});
						this.env.pos.synch.is_sync = false
					}
					if (self.env.pos.config.pos_stock_type == 'available'){
						$.each(prods, function( i, prd ){
							let loc_available = JSON.parse(prd.quant_text);
							prd['bi_available'] = 0;
							let total = 0;
							let out = 0;
							let inc = 0;
							$.each(loc_available, function( k, v ){
								if(location[0]['id'] == parseInt(k)){
									total += v[0];
									if(v[1]){
										out += v[1];
									}
									if(v[2]){
										inc += v[2];
									}
									let final_data = (total + inc)
									prd['bi_available'] = final_data;
									prd['virtual_available'] = final_data;
								}
							})
						});
						this.env.pos.synch.is_sync = false
					}
				}
				else{
					$.each(prods, function( i, prd ){
						prd['bi_on_hand'] = (prd.qty_available);
						prd['bi_available'] = (prd.virtual_available);
					});
				}
				return prods
			}
		};

	Registries.Component.extend(ProductsWidget, BiProductsWidget);

	return ProductsWidget;

});
