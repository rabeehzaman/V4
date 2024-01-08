# -*- coding: utf-8 -*-
{
    'name': 'POS Invoice Auto Check | Restrict POS Invoice Download',
    'version': '1.0',
    'author': 'Preway IT Solutions',
    'category': 'Point of Sale',
    'depends': ['point_of_sale'],
    'summary': 'This apps helps you select invoice button automatically on every order and restrict to download invoice pdf on pos screen | POS Auto Invoice | POS Invoice Auto Check | POS Default Invoicing | POS Auto invoice and Disable auto print | Restrict POS Invoice Download',
    'description': """
- POS Default invoice button is selected
- POS Auto invoicing
- POS Restrict to Download Invoice PDF
- POS Invoice automatically
    """,
    'data': [
        'views/pos_config_view.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pw_pos_invoice_and_restrict_download/static/src/js/payment_screen.js',
        ],
    },
    'price': 10.0,
    'currency': "EUR",
    'application': True,
    'installable': True,
    "license": "LGPL-3",
    'live_test_url': 'https://youtu.be/2tnhpjkjmbE',
    "images":["static/description/Banner.png"],
}
