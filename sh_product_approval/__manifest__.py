# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
{
    "name": "Product Approval",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "license": "OPL-1",
    "version": "16.0.2",
    "category": "Productivity",
    "summary": """
Product Approval, Product Management,Approve Product Module,
Product Manager Product Reject, Mass Product Approve,
Single Click Multiple Product Approve, Bulk Product Reject,
Single Click All Product Reject Odoo
""",
    "description": """
The product approval module will allow you to approve or
reject products only by-product manager,
Only approved products can be used in Sale, Purchase, Invoices,
CRM & Inventory, etc. When product create that will put it in the "Under Approval"
state by default and then after product manager
can move in approve or not approve state.
The approved product will appear in the whole odoo.
This module gives the facility to the product manager
to select multiple products means mass approval or mass reject products.
""",

    "depends": ["sale_management", "stock", "account"],
    "data": [
        "security/sh_product_approval_security.xml",
        "views/product_views.xml",
    ],
    "images": ["static/description/background.png"],
    "live_test_url": "https://youtu.be/tpShTDOts10",
    "installable": True,
    "auto_install": False,
    "application": True,
    "price": 20,
    "currency": "EUR"
}
