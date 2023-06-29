# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.


{
    "name": "POS Stock in Odoo",
    "version": "16.0.0.1",
    "category": "Point of Sale",
    "depends": ['base', 'sale_management', 'stock', 'point_of_sale'],
    "author": "BrowseInfo",
    'summary': 'Display POS Stock Quantity on POS screen stock Product stock in POS product stock Quantity POS Order stock POS Mobile POS Inventory management pos stocks pos item stock point of sale stock POS Product Warehouse Quantity pos product qty pos product Quantity',
    'price': 29,
    'currency': "EUR",
    "description": """
    odoo pos stock point of sales stocks pos stocks
    odoo pos inventory POS Stock - Available Qty
    odoo stock in pos odoo pos current stock of products

    odoo point of sales stock point of sale stocks point of sales stocks odoo
    odoo point of sales inventory point of sales Stock - Available Qty odoo
    odoo stock in point of sales odoo point of sales current stock of products odoo


    odoo point of sale stock point of sales stocks point of sale stocks odoo
    odoo point of sale inventory point of sale Stock - Available Qty odoo
    odoo stock in point of sale odoo point of sale current stock of products odoo

    pos 
    Purpose :- 
    odoo Display Stock in POS Display Stock Quantity on POS
    odoo POS warning stock Warning on POS 
    odoo POS stock management odoo Stock management on POS Product stock on POS
    odoo POS product stock POS product stock on hand Display product stock on POS
    odoo Point of sale stock odoo Display Stock in Point of Sales 
    odoo Display Stock Quantity on Point of Sales odoo Point of Sales warning stock  Warning on Point of Sales
    odoo Point of Sales stock management odoo Stock management on Point of Sales
    odoo Product stock on Point of Sales odoo Point of sales product stock 
    odoo Point of sales product stock on hand Display product stock on Point of Sales,

    odoo Point of sales stock odoo Display Stock in Point of Sales 
    odoo Display Stock Quantity on Point of Sale odoo Point of Sales warning stock  Warning on Point of Sales odoo
    odoo Point of Sale stock management odoo Stock management on Point of Sales odoo
    odoo Product stock on Point of Sale odoo Point of sales product stock odoo
    odoo Point of sale product stock on hand Display product stock on Point of Sale odoo
    """,
    "website": "https://www.browseinfo.in",
    "data": [
        'views/custom_pos_config_view.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'bi_pos_stock/static/src/css/stock.css',
            'bi_pos_stock/static/src/js/SyncStock.js',
            'bi_pos_stock/static/src/js/models.js',
            'bi_pos_stock/static/src/js/Chrome.js',
            'bi_pos_stock/static/src/js/Screens/ProductScreen.js',
            'bi_pos_stock/static/src/js/Screens/ProductsWidget.js',
            'bi_pos_stock/static/src/xml/**/*',
        ],
    },
    "auto_install": False,
    "installable": True,
    "live_test_url": 'https://youtu.be/X1GSrJl9iWY',
    "images": ['static/description/Banner.gif'],
    'license': 'OPL-1',
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
