# -*- coding: utf-8 -*-
{
    'name': "POS Internal Transfer | POS Stock Transfer",
    'version': '16.0.0',
    'summary': """Create Internal Transfer from POS""",
    'description': """This module allows to create internal transfer from POS, You can send/receive stock between shops | Transfer stock between shops | POS Internal Transfer in Odoo | Point Of Sale Stock Transfer | Stock Transfer From Point Of Sale | Stock Transfer From POS To Internal Locationr""",
    'author': "Preway IT Solutions",
    'category': 'Point of Sale',
    'depends': [
        'point_of_sale',
    ],
    'data': [
        'views/pos_session_view.xml',
        'views/pos_config_view.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pw_pos_stock_transfer/static/src/css/pos.css',
            'pw_pos_stock_transfer/static/src/input_popups/STCustomMsgPopup.js',
            'pw_pos_stock_transfer/static/src/input_popups/StockTransferPopup.js',
            'pw_pos_stock_transfer/static/src/js/TransferButton.js',
            'pw_pos_stock_transfer/static/src/xml/**/*',
        ],
    },
    'price': 40.0,
    'currency': "EUR",
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
    'live_test_url': 'https://youtu.be/ZGOhU5uxcBg',
    "images":["static/description/Banner.png"],
}
