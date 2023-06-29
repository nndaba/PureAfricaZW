# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import models


class PosSession(models.Model):
	_inherit = 'pos.session'



	def _loader_params_product_product(self):
		result = super()._loader_params_product_product()
		result['search_params']['fields'].extend(['type','virtual_available',
					'qty_available','incoming_qty','outgoing_qty','quant_text'])
		return result



	def _pos_ui_models_to_load(self):
		result = super()._pos_ui_models_to_load()
		new_model = 'stock.location'
		if new_model not in result:
			result.append(new_model)
		return result


	def _loader_params_stock_location(self):
		if (self.config_id.show_stock_location == 'specific'):
			return {
				'search_params': {
					'domain': [('id', 'in', self.config_id.stock_location_id.ids)],
					'fields': [
						'id','name',
					],
				}
			}    
		else:
			return {
				'search_params': {
					'domain': [('id', 'in', self.config_id.stock_location_id.ids)],
					'fields': [
						'id','name',
					],
				}
			}
		

	def _get_pos_ui_stock_location(self, params):
		return self.env['stock.location'].search_read(**params['search_params'])
