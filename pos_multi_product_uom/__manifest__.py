# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################
{
    "name"          :  "POS Multi Unit Of Measure",
    "summary"       :  """This module allow to use multiple units of measure for products in point of sale.Measurment|Unit Of Measure|Multiple Units|Measurement of multi unit""",
    "category"      :  "Point Of Sale",
    "version"       :  "1.0.6",
    "sequence"      :  1,
    "author"        :  "Webkul Software Pvt. Ltd.",
    "license"       :  "Other proprietary",
    "website"       :  "https://store.webkul.com/",
    "description"   :  """POS Multi UOM, Multiple units, Product Multi UOM, Product Multi Units""",
    "live_test_url" :  "http://odoodemo.webkul.com/?module=pos_multi_product_uom&custom_url=/pos/auto",
    "depends"       :  ['pos_orders_all'],
    'data'          : ['views/views.xml'],
    "assets"        :  {
                            'point_of_sale._assets_pos': [
                                "pos_multi_product_uom/static/src/overrides/**/*",
                            ],
                        },
    "images"        :  ['static/description/Banner.png'],
    "application"   :  True,
    "installable"   :  True,
    "auto_install"  :  False,
    "price"         :  45,
    "currency"      :  "USD",
    "pre_init_hook" :  "pre_init_check",
}
