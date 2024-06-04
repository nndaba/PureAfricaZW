/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : <https://store.webkul.com/license.html/> */
odoo.define('pos_multi_cat.pos_multi_cat', function (require) {
	"use strict";
	var PosDB = require('point_of_sale.DB');
	var utils = require('web.utils');

	PosDB.include({
		add_products: function (products) {
			var stored_categories = this.product_by_category_id;
			if (!products instanceof Array) {
				products = [products];
			}
			for (var i = 0, len = products.length; i < len; i++) {
				var product = products[i];
				if (product.id in this.product_by_id) continue;
				if (product.available_in_pos) {
					var search_string = utils.unaccent(this._product_search_string(product));
					if (product.product_tmpl_id) {
						product.product_tmpl_id = product.product_tmpl_id[0];
					}
					if (product.pos_categ_id && product.pos_categ_id.length > 1) {
						var k = 0, product_cat_len = (product.pos_categ_id).length;
						do {
							var categ_id = product.pos_categ_id ? product.pos_categ_id[k] : this.root_category_id;
							if (!categ_id) {
								if (!stored_categories[0]) {
									stored_categories[0] = [];
								}
								stored_categories[0].push(product.id);
								if (this.category_search_string[0] === undefined) {
									this.category_search_string[0] = '';
								}
								this.category_search_string[0] += search_string;
								var ancestors = this.get_category_ancestors_ids(0) || [];
							} else {
								if (!stored_categories[categ_id]) {
									stored_categories[categ_id] = [];
								}
								stored_categories[categ_id].push(product.id);
								if (this.category_search_string[categ_id] === undefined) {
									this.category_search_string[categ_id] = '';
								}
								this.category_search_string[categ_id] += search_string;
								var ancestors = this.get_category_ancestors_ids(categ_id) || [];
							}
							k++;
						} while (k <= product_cat_len);
					}
					else {
						var categ_id =  product.pos_categ_id[0] ? product.pos_categ_id[0] : this.root_category_id;
						if (!stored_categories[categ_id]) {
							stored_categories[categ_id] = [];
						}
						stored_categories[categ_id].push(product.id);
						if (this.category_search_string[categ_id] === undefined) {
							this.category_search_string[categ_id] = '';
						}
						this.category_search_string[categ_id] += search_string;
						var ancestors = this.get_category_ancestors_ids(categ_id) || [];
					}

					for (var j = 0, jlen = ancestors.length; j < jlen; j++) {
						var ancestor = ancestors[j];
						if (!stored_categories[ancestor]) {
							stored_categories[ancestor] = [];
						}
						stored_categories[ancestor].push(product.id);
						if (this.category_search_string[ancestor] === undefined) {
							this.category_search_string[ancestor] = '';
						}
						this.category_search_string[ancestor] += search_string;
					}
				}
				this.product_by_id[product.id] = product;
				if (product.barcode) {
					this.product_by_barcode[product.barcode] = product;
				}
			}
		},
	});
});