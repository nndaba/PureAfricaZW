# -*- coding: utf-8 -*-
{
    'name': "fiscalization",

    'summary': """
        This module is responsible for fiscalizing invoices
        """,

    'description': """
        This module is responsible for fiscalizing invoices
    """,

    'author': "Telecontract pvt",
    'website': "www.telco.co.zw",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account'],

    # always loaded
    'data': [
        'security/fiscalization_security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/cron.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
