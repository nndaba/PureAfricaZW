# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
{
    "name" : "Manual Currency Exchange Rate on Invoice/Payment/Sale/Purchase in Odoo",
    "version" : "16.0.0.2",
    "depends" : ['base','account','purchase','sale_management','stock'],
    "author": "BrowseInfo",
    "summary": "Apps apply manual currency rate on invoice manual currency rate on payment manual currency rate on sales manual currency rate on purchase custom currency rate on invoice manual Currency Exchange Rate on Invoice custom Currency Exchange Rate on sales order",
    "description": """
    Odoo/OpenERP module for manul currency rate converter
    Currency Exchange Rate on Invoice/Payment/Sale/Purchase, manual multi currency process on invoice, multi currency payment
    Currency Exchange Rate on Payment/Sale/Purchase
    Manual Currency Exchange Rate on invoice payment
    Manual Currency Rate on invoice payment
    Currency Exchange Rate on Sales order
    Currency Exchange Rate on Sale order
    Currency Exchange Rate on Purchase Order
    Apply Manual Currency Exchange Rate on Invoice/Payment/Sale/Purchase
    Apply Manual Currency Exchange Rate on Payment
    Apply Manual Currency Exchange Rate on Sale Order
    Apply Manual Currency Exchange Rate on Purchase OrderCurrency Exchange Rate on Sale/Purchase
    Currency Exchange Rate on Sales order
    Currency Exchange Rate on Purchase Order
    Apply Manual Currency Exchange Rate on Sale/Purchase
    Apply Manual Currency Exchange Rate on Sale Order
	Currency Exchange Rate on Invoice/Payment, manual multi currency process on invoice, multi currency payment
    Currency Exchange Rate on Payment
    Manual Currency Exchange Rate on invoice payment , Currency Exchange Rate for invoice , Currency Exchange Rate in invoice , invoice Currency Exchange Rate , invoice
    Manual Currency Rate on invoice payment Exchange Rate on 
    Apply Manual Currency Exchange Rate on Invoice/Payment
    Apply Manual Currency Exchange Rate on Payment
	add Manual Currency Exchange Rate
	multiple currency rate , many currency 
    Exchange Currency rate
    custom exchange rate
    Rates of Exchange 
    Exchange Rates
    custom exchange rate
    Customs Exchange Rate
    Conversion rates
    dollar exchange rate
    real exchange rate
    Currency Exchange Rate Update
    Currency Rate Update
    Currency Rates Update
    multi-currency rates
    multicurrency exchanges rates
    exchange rate
    exchange rates

    Apply Manual Currency Rate on Invoice/Payment
    Apply Manual Currency Rate on Payment
    multi-currency process on invoice, multi-currency payment
    currency converter on Odoo
    invoice currency rate
    Manual Exchange rate of Currency apply
    manual currency rate on invoice
    currency rate apply manually
    Apply Manual Currency Exchange Rate on Purchase Order

    Apply Manual Currency Rate on Sale/Purchase
    Apply Manual Currency Rate on Sale Order
    Apply Manual Currency Rate on Purchase Order
    multi-currency process on invoice, multi-currency payment
    currency converter on Odoo
    invoice currency rate

    Apply Manual Currency Rate on Invoice/Payment/Sale/Purchase
    Apply Manual Currency Rate on Payment
    Apply Manual Currency Rate on Sale Order
    Apply Manual Currency Rate on Purchase Order
    multi-currency process on invoice, multi-currency payment
    currency converter on Odoo
    invoice currency rate
    Manual Exchange rate of Currency apply
    manual currency rate on invoice
    currency rate apply manually


    odoo manual currency rate converter Currency Exchange Rate on Sale Purchase manual multi currency process on invoice multi currency payment
    odoo Currency Exchange Rate on Sale and Purchase Currency Exchange Rate on Sales order Currency Exchange Rate on Purchase Order
    odoo Apply Manual Currency Exchange Rate on Sale Purchase Apply Manual Currency Exchange Rate on Sale Order
    odoo Currency Exchange Rate on Invoice and account Payment manual multi currency process on invoice
    odoo multi currency payment Currency Exchange Rate on Payment
    odoo Manual Currency Exchange Rate on invoice payment Currency Exchange Rate for invoice 
    odoo Currency Exchange Rate in invoice odoo invoice Currency Exchange Rate invoice
    odoo Manual Currency Rate on invoice payment Exchange Rate odoo Apply Manual Currency Exchange Rate on payment
    odoo Apply Manual Currency Exchange Rate on Payment add Manual Currency Exchange Rate
    

    odoo Apply Manual Currency Rate on Invoice Payment Apply Manual Currency Rate on Payment
    odoo multi-currency process on invoice multi-currency payment currency converter on Odoo
    odoo invoice currency rate Manual Exchange rate of Currency apply manual currency rate on invoice
    odoo currency rate apply manually Apply Manual Currency Exchange Rate on Purchase Order

    odoo Apply Manual Currency Rate on Sale and Purchase Apply Manual Currency Rate on Sale Order
    odoo Apply Manual Currency Rate on Purchase Order multi-currency process on invoice multi-currency payment
    odoo currency converter on Odoo invoice currency rate currency rate apply manually Exchange Currency rate
    odoo custom exchange rate odoo Rates of Exchange odoo Exchange Rates custom exchange rate
    odoo Customs Exchange Rate Conversion rates dollar exchange rate
    odoo real exchange rate Currency Exchange Rate Update Currency Rate Update Currency Rates Update
    odoo multi-currency rates multicurrency exchanges rates odoo exchange rate
    odoo manual exchange rates on account payment Account Invoice Currency Rate
    odoo currency conversation rate Invoice Currency Rate currency rate on invoice auto currency rates

        Odoo/OpenERP module for odoo manual currency rate converter
    odoo Currency Exchange Rate on Invoice Payment manual multi currency process on invoice multi currency payment
    odoo Currency Exchange Rate on Payment
    odoo Manual Currency Exchange Rate on invoice payment Currency Exchange Rate for invoice Currency Exchange Rate in invoice 
    odoo invoice Currency Exchange Rate invoice
    odoo Manual Currency Rate on invoice payment Exchange Rate Apply Manual Currency Exchange Rate on Invoice/Payment
    odoo Apply Manual Currency Exchange Rate on Payment
    odoo add Manual Currency Exchange Rate Apply Manual Currency Rate on Invoice Payment Apply Manual Currency Rate on Payment
    odoo multi-currency process on invoice multi-currency payment currency converter on Odoo
    odoo invoice currency rate Manual Exchange rate of Currency apply manual currency rate on invoice
    odoo currency rate apply manually multiple currency rate many currency Exchange Currency rate custom exchange rate
    odoo Rates of Exchange Exchange Rates custom exchange rate 
    odoo Customs Exchange Rate Conversion rates for invoice and payment
    odoo dollar exchange rate real exchange rate Currency Exchange Rate Update
    odoo Currency Rate Update Currency Rates Update multi-currency rates multicurrency exchanges rates
    odoo exchange rate exchange rates Account Invoice Currency Rate currency conversation rate
    odoo Invoice Currency Rate currency rate on invoice auto currency rates
    Default Odoo takes exchange rate from the currency configuration/menu and change currency rate daily process is very hard that change currency rate everyday from currency menu for each currency. With help of this Odoo apps you will have option to set Currency Exchange Rates manually/directly on customer invoices, vendor bills, sales order, purchase order and account payment on each record and its cover whole workflow of Odoo ERP with apply manual currency exchange rates. After installing this Odoo module you will extra field to apply manual exchange rate on all documents(SO, PO, Invoices, Payments) after apply manual exchange rate everything converted with this applied manual exchange rate i.e product price change on order lines and invoice line, accounting entries generated with this assigned exchange rate.
    This Odoo apps provide unique feature for Currency Exchange Rate Update manually for different currency such as Dollar, Euro or almost all directly from the transaction records i.e sales purchase, invoice and payment.
    if you are using Odoo multi-currency working to provide invoices, sale order, purchase order to customers from different countries along with currency rates according to their country? For Odoo This module is designed to provide currency rate exchange in real time can be really useful Currency Exchange Rates in Odoo. 

    """,
    "price": 22,
    "currency": "EUR",
    'category': 'Accounting',
    "website" : "https://www.browseinfo.in",
    "data" :[
             "views/customer_invoice.xml",
             "views/account_payment_view.xml",
             "views/purchase_view.xml",
             "views/sale_view.xml",
        ],
    'qweb':[],
    "auto_install": False,
    "installable": True,
    'live_test_url':'https://youtu.be/nRdIuuxi9yI',
	"images":['static/description/Banner.gif'],
    "license": "OPL-1",
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
