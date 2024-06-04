# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################
{
    "name"              :  "POS Multi Category",
    "summary"           :  """The module allows the user to assign multiple POS categories to
                                 the POS products. The products can then be selected appropriately even if they fall in multiple categories.Manage POS category|Multiple POS categories|Product category POS|Assign product categories.
                            """,
    "category"          :  "Point of Sale",
    "version"           :  "1.1.1",
    "sequence"          :  1,
    "author"            :  "Webkul Software Pvt. Ltd.",
    "license"           :  "Other proprietary",
    "website"           :  "https://store.webkul.com/Odoo-POS-Multi-Category.html",
    "description"       :  """Odoo POS Multi Category POS category""",
    "live_test_url"     :  "http://odoodemo.webkul.com/?module=pos_multi_cat&custom_url=/pos/auto",
    "depends"           :  ['point_of_sale'],
    "data"              :  ['views/pos_multi_cat_view.xml', ],
    "demo"              :  ['data/pos_multi_cat_demo.xml'],
    "images"            :  ['static/description/Banner.png'],
    "application"       :  True,
    "installable"       :  True,
    "assets"            :  {
                                'point_of_sale.assets': [
                                    "/pos_multi_cat/static/src/js/pos_multi_cat.js", 
                                ],
                            },
    "auto_install"      :  False,
    "price"             :  49,
    "currency"          : "USD",
    "pre_init_hook"     :  "pre_init_check",
    "post_init_hook"    :  "post_product_fetch",
}
