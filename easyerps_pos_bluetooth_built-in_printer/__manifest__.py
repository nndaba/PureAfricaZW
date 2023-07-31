# -- coding: utf-8 --
{
    'name': "POS Bluetooth/Built-in Printer",
    'support': "support@easyerps.com",
    'license': "OPL-1",
    'price': 199,
    'currency': "USD",
    'summary': """
        This module Allows you to print POS receipts directly using Bluetooth, Built-in, USB or IP Printer on SUNMI/Android devices
        """,
    'author': "EasyERPS",
    'website': "https://EasyERPS.com",
    'category': 'Point of Sale',
    'version': '16.1.0',
    'depends': ['base', 'point_of_sale'],
    'data': [
        'views/views.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'EasyERPS_pos_bluetooth_built-in_printer-16/static/src/js/*.js',
             ('after','point_of_sale/static/src/scss/pos.scss' ,'EasyERPS_pos_bluetooth_built-in_printer-16/static/src/css/BluetoothPrinterReceiptScreen.css'),
            'EasyERPS_pos_bluetooth_built-in_printer-16/static/src/xml/*.xml',
        ],

    },
    'images': ['images/main_screenshot.png'],
}
