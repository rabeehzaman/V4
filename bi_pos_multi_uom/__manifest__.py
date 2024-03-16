# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
{
    'name': "POS Multi UOM",
    'version': '17.0.0.0',
    'category': 'Point of Sale',
    'summary': "Multi UOM for Products in POS product multi uom on point of sales multi uom point of sales multiple uom allow multiple uom on pos multiple uom on point of sale multi uom pos different uom on pos multi unit of measure point of sale multi unit of measure",
    'description': """ 

        Multi UOM for Products in POS in odoo,
        Add Multi UOM for Product in odoo,
        POS Multi UOM in odoo,
        Select Multi UOM on POS in odoo,
        Multi UOM on POS Receipt in odoo,
        Multi UOM on POS Order in odoo,

    """,
    'author': 'BrowseInfo',
    "price": 19,
    "currency": 'EUR',
    'website': 'https://www.browseinfo.com',
    'depends': ['base', 'point_of_sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/point_of_sale.xml',
        'views/pos_config.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'bi_pos_multi_uom/static/src/app/models.js',
            'bi_pos_multi_uom/static/src/app/pos_store.js',
            'bi_pos_multi_uom/static/src/app/uom_button.js',
            'bi_pos_multi_uom/static/src/app/uom_button.xml',
            'bi_pos_multi_uom/static/src/app/uom_popup.js',
            'bi_pos_multi_uom/static/src/app/uom_popup.xml',
           
        ],
    },
    'license': 'OPL-1',
    'installable': True,
    'auto_install': False,
    'live_test_url':'https://www.youtube.com/watch?v=WaDJf3AV_DI',
    "images":['static/description/Banner.gif'],
}
