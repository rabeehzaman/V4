{
    'name': "Zoho Analytics Odoo Integration addon",
    'summary': """
        The addon helps us to get the synchronisesd records between zoho analaytics and odoo.""",
    'description': """
        The addon helps us to get the synchronisesd records between zoho analaytics and odoo.
    """,
    'depends': ['base_setup'],
    'author': 'Zoho Analytics',
    'website': 'http://www.zoho.com/analytics',
    'category': 'Extra Tools',
    'license': "LGPL-3",
    'data': [
        'views/zadeleted_records_views.xml',
        'security/ir.model.access.csv',
    ],
    'auto_install': False,
    'installable': True,
    'application': False,
}
