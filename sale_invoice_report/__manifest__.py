# -*- coding: utf-8 -*-

{
    "name": "Sale Invoice Report",
    'version': '17.0.0.0',
    "category": 'Invoice Report',
    "summary": ' Invoice Report',
    'sequence': 3,
    "description": """"  """,
    "author": "Usama Shakeel",
    "website": "",
    'license': 'LGPL-3',
    'depends': ['base','contacts', 'account'],
    'data': [

        'report/sales_tax_invoice.xml',
        # 'views/sales_commercel_invoice.xml',

    ],

    "installable": True,
    "application": True,
    "auto_install": False,
}

