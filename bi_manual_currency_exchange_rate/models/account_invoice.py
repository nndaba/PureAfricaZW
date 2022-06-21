# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models,api,_
from odoo.exceptions import UserError, Warning, ValidationError



class stock_move(models.Model):
	_inherit = 'stock.move'

	def _create_in_svl(self, forced_quantity=None):
		"""Create a `stock.valuation.layer` from `self`.

		:param forced_quantity: under some circunstances, the quantity to value is different than
			the initial demand of the move (Default value = None)
		"""

		rec  = super(stock_move, self)._create_in_svl(forced_quantity=None)
		for rc in rec:
			for line in self:
				if line.purchase_line_id :
					if line.purchase_line_id.order_id.purchase_manual_currency_rate_active:
						price_unit = line.purchase_line_id.order_id.currency_id.round((line.purchase_line_id.price_unit)/line.purchase_line_id.order_id.purchase_manual_currency_rate)

						rc.write({'unit_cost' : price_unit,'value' :price_unit * rc.quantity,'remaining_value' : price_unit * rc.quantity})
		return rec


	def _prepare_account_move_vals(self, credit_account_id, debit_account_id, journal_id, qty, description, svl_id, cost):
		res = super(stock_move, self)._prepare_account_move_vals( credit_account_id, debit_account_id, journal_id, qty, description, svl_id, cost)
	
		if self.purchase_line_id.order_id.purchase_manual_currency_rate_active:
			res.update({
						"manual_currency_rate_active" : self.purchase_line_id.order_id.purchase_manual_currency_rate_active,
						"manual_currency_rate" : self.purchase_line_id.order_id.purchase_manual_currency_rate,
						"currency_id" : self.purchase_line_id.order_id.currency_id.id,
						});

		if self.sale_line_id.order_id.sale_manual_currency_rate_active:
			res.update({
						"manual_currency_rate_active" : self.sale_line_id.order_id.sale_manual_currency_rate_active,
						"manual_currency_rate" : self.sale_line_id.order_id.sale_manual_currency_rate,
						"currency_id" : self.sale_line_id.order_id.currency_id.id,
						});

		return res


	def _prepare_account_move_line(self, qty, cost, credit_account_id, debit_account_id, description):
		"""
		Generate the account.move.line values to post to track the stock valuation difference due to the
		processing of the given quant.
		"""
		self.ensure_one()

		# the standard_price of the product may be in another decimal precision, or not compatible with the coinage of
		# the company currency... so we need to use round() before creating the accounting entries.
		debit_value = self.company_id.currency_id.round(cost)
		credit_value = debit_value

		valuation_partner_id = self._get_partner_id_for_valuation_lines()

		if self.purchase_line_id.order_id.purchase_manual_currency_rate_active:
			debit_value = self.purchase_line_id.order_id.currency_id.round((self.purchase_line_id.price_unit*qty)/self.purchase_line_id.order_id.purchase_manual_currency_rate or 1)
			credit_value = debit_value
			res = [(0, 0, line_vals) for line_vals in self._generate_valuation_lines_data(valuation_partner_id, qty, debit_value, credit_value, debit_account_id, credit_account_id, description).values()]

		else:
			res = [(0, 0, line_vals) for line_vals in self._generate_valuation_lines_data(valuation_partner_id, qty, debit_value, credit_value, debit_account_id, credit_account_id, description).values()]

		if self.sale_line_id.order_id.sale_manual_currency_rate_active:
			credit_value = 	self.sale_line_id.order_id.currency_id.round((self.sale_line_id.price_unit*qty)/self.sale_line_id.order_id.sale_manual_currency_rate or 1)
			debit_value = credit_value
			res = [(0, 0, line_vals) for line_vals in self._generate_valuation_lines_data(valuation_partner_id, qty, debit_value, credit_value, debit_account_id, credit_account_id, description).values()]
		else:
			res = [(0, 0, line_vals) for line_vals in self._generate_valuation_lines_data(valuation_partner_id, qty, debit_value, credit_value, debit_account_id, credit_account_id, description).values()]

		return res


	def _generate_valuation_lines_data(self, partner_id, qty, debit_value, credit_value, debit_account_id, credit_account_id, description):
		""" Overridden from stock_account to support amount_currency on valuation lines generated from po
		"""
		self.ensure_one()

		rslt = super(stock_move, self)._generate_valuation_lines_data(partner_id, qty, debit_value, credit_value, debit_account_id, credit_account_id, description)
		if self.purchase_line_id and self.purchase_line_id.order_id.purchase_manual_currency_rate_active and self.purchase_line_id.order_id.purchase_manual_currency_rate > 0:
			purchase_currency = self.purchase_line_id.currency_id
			if purchase_currency != self.company_id.currency_id:
				# Do not use price_unit since we want the price tax excluded. And by the way, qty
				# is in the UOM of the product, not the UOM of the PO line.
				purchase_price_unit = (
					self.purchase_line_id.price_subtotal / self.purchase_line_id.product_uom_qty
					if self.purchase_line_id.product_uom_qty
					else self.purchase_line_id.price_unit
				)
				currency_move_valuation = purchase_currency.round(purchase_price_unit * abs(qty))
				rslt['credit_line_vals']['amount_currency'] = rslt['credit_line_vals']['credit'] and -currency_move_valuation or currency_move_valuation
				rslt['credit_line_vals']['currency_id'] = purchase_currency.id
				rslt['debit_line_vals']['amount_currency'] = rslt['debit_line_vals']['credit'] and -currency_move_valuation or currency_move_valuation
				rslt['debit_line_vals']['currency_id'] = purchase_currency.id
		
		if self.sale_line_id and self.sale_line_id.order_id.sale_manual_currency_rate_active and self.sale_line_id.order_id.sale_manual_currency_rate > 0:
			sale_currency = self.sale_line_id.currency_id
			if sale_currency != self.company_id.currency_id:
				# Do not use price_unit since we want the price tax excluded. And by the way, qty
				# is in the UOM of the product, not the UOM of the PO line.
				sale_price_unit = (
					self.sale_line_id.price_subtotal / self.sale_line_id.product_uom_qty
					if self.sale_line_id.product_uom_qty
					else self.sale_line_id.price_unit
				)
				currency_move_valuation = sale_currency.round(sale_price_unit * abs(qty))
				rslt['credit_line_vals']['amount_currency'] = rslt['credit_line_vals']['credit'] and -currency_move_valuation or currency_move_valuation
				rslt['credit_line_vals']['currency_id'] = sale_currency.id
				rslt['debit_line_vals']['amount_currency'] = rslt['debit_line_vals']['credit'] and -currency_move_valuation or currency_move_valuation
				rslt['debit_line_vals']['currency_id'] = sale_currency.id
		
		return rslt



class account_invoice_line(models.Model):
	_inherit ='account.move.line'



	@api.model
	def _get_fields_onchange_subtotal_model(self, price_subtotal, move_type, currency, company, date):
		''' This method is used to recompute the values of 'amount_currency', 'debit', 'credit' due to a change made
		in some business fields (affecting the 'price_subtotal' field).

		:param price_subtotal:  The untaxed amount.
		:param move_type:       The type of the move.
		:param currency:        The line's currency.
		:param company:         The move's company.
		:param date:            The move's date.
		:return:                A dictionary containing 'debit', 'credit', 'amount_currency'.
		'''
		if move_type in self.move_id.get_outbound_types():
			sign = 1
		elif move_type in self.move_id.get_inbound_types():
			sign = -1
		else:
			sign = 1

		amount_currency = price_subtotal * sign

		if self.move_id.manual_currency_rate_active and self.move_id.manual_currency_rate > 0:
			currency_rate = company.currency_id.rate / self.move_id.manual_currency_rate
			balance = amount_currency*currency_rate

		else:
			balance = currency._convert(amount_currency, company.currency_id, company,
		                                    date or fields.Date.context_today(self))

		return {
		    'amount_currency': amount_currency,
		    'currency_id': currency.id,
		    'debit': balance > 0.0 and balance or 0.0,
		    'credit': balance < 0.0 and -balance or 0.0,
		}



	@api.onchange('amount_currency')
	def _onchange_amount_currency(self):
		for line in self:
			company = line.move_id.company_id
			if line.move_id.manual_currency_rate_active and line.move_id.manual_currency_rate > 0:
				currency_rate = company.currency_id.rate / line.move_id.manual_currency_rate 
				balance = line.amount_currency*currency_rate

			else:
				balance = line.currency_id._convert(line.amount_currency, company.currency_id, company, line.move_id.date or fields.Date.context_today(line))
			line.debit = balance if balance > 0.0 else 0.0
			line.credit = -balance if balance < 0.0 else 0.0

			if not line.move_id.is_invoice(include_receipts=True):
				continue
			line.update(line._get_fields_onchange_balance())
			line.update(line._get_price_total_and_subtotal())


	@api.onchange('currency_id')
	def _onchange_currency(self):
		for line in self:
			company = line.move_id.company_id

			if line.move_id.is_invoice(include_receipts=True):
				line._onchange_price_subtotal()
			elif not line.move_id.reversed_entry_id:
				if line.move_id.manual_currency_rate_active and line.move_id.manual_currency_rate > 0:
					currency_rate = company.currency_id.rate / line.move_id.manual_currency_rate 
					balance = line.amount_currency*currency_rate
				else:
					balance = line.currency_id._convert(line.amount_currency, company.currency_id, company, line.move_id.date or fields.Date.context_today(line))
				line.debit = balance if balance > 0.0 else 0.0
				line.credit = -balance if balance < 0.0 else 0.0



	def _get_computed_price_unit(self):
		res = super(account_invoice_line, self)._get_computed_price_unit()
		if self.move_id.manual_currency_rate_active and self.move_id.manual_currency_rate > 0:
			price_unit = res;
			currency_rate = self.move_id.manual_currency_rate/self.move_id.company_id.currency_id.rate
			if self.move_id.is_sale_document(include_receipts=True):
				price_unit = self.product_id.lst_price
			elif self.move_id.is_purchase_document(include_receipts=True):
				price_unit = self.product_id.standard_price
			else:
				pass;
			return price_unit * currency_rate
		return res



        
class account_invoice(models.Model):
	_inherit ='account.move'

	manual_currency_rate_active = fields.Boolean('Apply Manual Exchange')
	manual_currency_rate = fields.Float('Rate', digits=(12, 6))


	@api.constrains("manual_currency_rate")
	def _check_manual_currency_rate(self):
		for record in self:
			if record.manual_currency_rate_active:
				if record.manual_currency_rate == 0:
					raise UserError(_('Exchange Rate Field is required , Please fill that.'))

	@api.onchange('manual_currency_rate_active', 'currency_id')
	def check_currency_id(self):
		if self.manual_currency_rate_active:
			if self.currency_id == self.company_id.currency_id:
				self.manual_currency_rate_active = False
				raise UserError(_('Company currency and invoice currency same, You can not add manual Exchange rate for same currency.'))



	def _recompute_tax_lines(self, recompute_tax_base_amount=False):
		self.ensure_one()
		in_draft_mode = self != self._origin

		def _serialize_tax_grouping_key(grouping_dict):
			return '-'.join(str(v) for v in grouping_dict.values())

		def _compute_base_line_taxes(base_line):
			move = base_line.move_id

			if move.is_invoice(include_receipts=True):
				handle_price_include = True
				sign = -1 if move.is_inbound() else 1
				quantity = base_line.quantity
				is_refund = move.move_type in ('out_refund', 'in_refund')
				price_unit_wo_discount = sign * base_line.price_unit * (1 - (base_line.discount / 100.0))
			else:
				handle_price_include = False
				quantity = 1.0
				tax_type = base_line.tax_ids[0].type_tax_use if base_line.tax_ids else None
				is_refund = (tax_type == 'sale' and base_line.debit) or (tax_type == 'purchase' and base_line.credit)
				price_unit_wo_discount = base_line.amount_currency

			return base_line.tax_ids._origin.with_context(force_sign=move._get_tax_force_sign()).compute_all(
			    price_unit_wo_discount,
			    currency=base_line.currency_id,
			    quantity=quantity,
			    product=base_line.product_id,
			    partner=base_line.partner_id,
			    is_refund=is_refund,
			    handle_price_include=handle_price_include,
			    include_caba_tags=move.always_tax_exigible,
			)

		taxes_map = {}

		# ==== Add tax lines ====
		to_remove = self.env['account.move.line']
		for line in self.line_ids.filtered('tax_repartition_line_id'):
			grouping_dict = self._get_tax_grouping_key_from_tax_line(line)
			grouping_key = _serialize_tax_grouping_key(grouping_dict)
			if grouping_key in taxes_map:
				to_remove += line
			else:
				taxes_map[grouping_key] = {
			        'tax_line': line,
			        'amount': 0.0,
			        'tax_base_amount': 0.0,
			        'grouping_dict': False,
			    }
		if not recompute_tax_base_amount:
			self.line_ids -= to_remove

        # ==== Mount base lines ====
		for line in self.line_ids.filtered(lambda line: not line.tax_repartition_line_id):
			# Don't call compute_all if there is no tax.
			if not line.tax_ids:
				if not recompute_tax_base_amount:
					line.tax_tag_ids = [(5, 0, 0)]
				continue

			compute_all_vals = _compute_base_line_taxes(line)

			# Assign tags on base line
			if not recompute_tax_base_amount:
				line.tax_tag_ids = compute_all_vals['base_tags'] or [(5, 0, 0)]

			for tax_vals in compute_all_vals['taxes']:
				grouping_dict = self._get_tax_grouping_key_from_base_line(line, tax_vals)
				grouping_key = _serialize_tax_grouping_key(grouping_dict)

				tax_repartition_line = self.env['account.tax.repartition.line'].browse(tax_vals['tax_repartition_line_id'])
				tax = tax_repartition_line.invoice_tax_id or tax_repartition_line.refund_tax_id

				taxes_map_entry = taxes_map.setdefault(grouping_key, {
			        'tax_line': None,
			        'amount': 0.0,
			        'tax_base_amount': 0.0,
			        'grouping_dict': False,
			    })
				taxes_map_entry['amount'] += tax_vals['amount']
				taxes_map_entry['tax_base_amount'] += self._get_base_amount_to_display(tax_vals['base'], tax_repartition_line, tax_vals['group'])
				taxes_map_entry['grouping_dict'] = grouping_dict

		taxes_map = self._preprocess_taxes_map(taxes_map)

		for taxes_map_entry in taxes_map.values():
			# The tax line is no longer used in any base lines, drop it.
			if taxes_map_entry['tax_line'] and not taxes_map_entry['grouping_dict']:
				if not recompute_tax_base_amount:
					self.line_ids -= taxes_map_entry['tax_line']
				continue

			currency = self.env['res.currency'].browse(taxes_map_entry['grouping_dict']['currency_id'])

			# Don't create tax lines with zero balance.
			if currency.is_zero(taxes_map_entry['amount']):
				if taxes_map_entry['tax_line'] and not recompute_tax_base_amount:
					self.line_ids -= taxes_map_entry['tax_line']
				continue

			# tax_base_amount field is expressed using the company currency.
			if self.manual_currency_rate_active and self.manual_currency_rate > 0:
				currency_rate = self.company_currency_id.rate / self.manual_currency_rate
				tax_base_amount = taxes_map_entry['tax_base_amount'] * currency_rate
			else:
				tax_base_amount = currency._convert(taxes_map_entry['tax_base_amount'], self.company_currency_id, self.company_id, self.date or fields.Date.context_today(self))

			# Recompute only the tax_base_amount.
			if recompute_tax_base_amount:
				if taxes_map_entry['tax_line']:
					taxes_map_entry['tax_line'].tax_base_amount = tax_base_amount
				continue

			if self.manual_currency_rate_active and self.manual_currency_rate > 0:
				currency_rate = self.company_currency_id.rate / self.manual_currency_rate
				balance = taxes_map_entry['amount'] * currency_rate
			else:
				balance = currency._convert(
				    taxes_map_entry['amount'],
				    self.company_currency_id,
				    self.company_id,
				    self.date or fields.Date.context_today(self),
				)
			to_write_on_line = {
			    'amount_currency': taxes_map_entry['amount'],
			    'currency_id': taxes_map_entry['grouping_dict']['currency_id'],
			    'debit': balance > 0.0 and balance or 0.0,
			    'credit': balance < 0.0 and -balance or 0.0,
			    'tax_base_amount': tax_base_amount,
			}

			if taxes_map_entry['tax_line']:
				taxes_map_entry['tax_line'].update(to_write_on_line)
			else:
				# Create a new tax line.
				create_method = in_draft_mode and self.env['account.move.line'].new or self.env['account.move.line'].create
				tax_repartition_line_id = taxes_map_entry['grouping_dict']['tax_repartition_line_id']
				tax_repartition_line = self.env['account.tax.repartition.line'].browse(tax_repartition_line_id)
				tax = tax_repartition_line.invoice_tax_id or tax_repartition_line.refund_tax_id
				taxes_map_entry['tax_line'] = create_method({
				    **to_write_on_line,
				    'name': tax.name,
				    'move_id': self.id,
				    'partner_id': line.partner_id.id,
				    'company_id': line.company_id.id,
				    'company_currency_id': line.company_currency_id.id,
				    'tax_base_amount': tax_base_amount,
				    'exclude_from_invoice_tab': True,
				    **taxes_map_entry['grouping_dict'],
				})

			if in_draft_mode:
				taxes_map_entry['tax_line'].update(taxes_map_entry['tax_line']._get_fields_onchange_balance(force_computation=True))


