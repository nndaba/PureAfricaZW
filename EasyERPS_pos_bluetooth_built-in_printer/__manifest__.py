# -*- coding: utf-8 -*-
{
    'name': "POS Bluetooth/Built-in Printer",
    'support': "support@easyerps.com",
    'license': "OPL-1",
    'price': 200,
    'currency': "USD",
    'summary': """
        This module Allows you to print POS receipts directly using Bluetooth, Built-in, USB or IP Printer on SUNMI/Android devices
        """,
    'author': "EasyERPS",
    'website': "https://EasyERPS.com",
    'category': 'Point of Sale',
    'version': '15.1.2',
    'depends': ['base', 'point_of_sale'],
    'data': [
        'views/views.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'EasyERPS_pos_bluetooth_built-in_printer/static/src/js/BluetoothPrinterReceiptScreen.js',
            'EasyERPS_pos_bluetooth_built-in_printer/static/src/css/BluetoothPrinterReceiptScreen.css',
            'EasyERPS_pos_bluetooth_built-in_printer/static/src/js/CategoryReceipt.js',
            'EasyERPS_pos_bluetooth_built-in_printer/static/src/js/LabelReceipt.js',
            'EasyERPS_pos_bluetooth_built-in_printer/static/src/js/Models.js',
            'EasyERPS_pos_bluetooth_built-in_printer/static/src/js/ReprintReceiptScreen.js',
            'EasyERPS_pos_bluetooth_built-in_printer/static/src/js/PaymentScreen.js',
            'EasyERPS_pos_bluetooth_built-in_printer/static/src/js/SaleDetailsButton.js',
        ],
        'web.assets_qweb': [
            'EasyERPS_pos_bluetooth_built-in_printer/static/src/xml/**/*',
        ],
    },
    'images': ['images/main_screenshot.png'],
}
