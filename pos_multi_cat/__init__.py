# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   License URL : <https://store.webkul.com/license.html/>
#
#################################################################################
from . import models
from odoo import api, SUPERUSER_ID

def pre_init_check(cr):
    from odoo.service import common
    from odoo.exceptions import UserError
    version_info = common.exp_version()
    server_serie = version_info.get('server_serie')
    if server_serie != '16.0':
        raise UserError(
            'Module support Odoo series 16.0 found {}.'.format(server_serie))
    return True

def post_product_fetch(cr,registry):
    """
        To set the default category of product in the pos category which was not 
        present earlier . Before this change, we had to manually set the category of product 
        which used to be set by default, this was creating inconvenience to the user. And if the no. of products in POS where in large quantity, this process would have been very time consuming.
    """
    env = api.Environment(cr,SUPERUSER_ID,{})
    cr.execute("SELECT id,name,pos_categ_id FROM product_template")
    db_product_data = cr.fetchall()
    products_data = env['product.template'].search([])

    prod_db_cat_dict = {}
    for db_prod in db_product_data:
        if db_prod[2]:
            prod_db_cat_dict[db_prod[0]] = db_prod[2]

    for product in products_data:
        if product.id in prod_db_cat_dict:
            product.write({
                'pos_categ_id':[(6, 0,[prod_db_cat_dict[product.id]])]
            })   
