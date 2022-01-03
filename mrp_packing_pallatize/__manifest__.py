# -*- coding: utf-8 -*-
{
    'name': "Manufacturing Pack After Manufacture",
    'summary': """ Manufacturing Pack After Manufacture """,
    'description': """
        Manufacturing Pack After Manufacture
    """,
    'author': "PPTS(India) Pvt Ltd",
    'website': "https://www.pptssolutions.com",
    'category': 'MRP',
    'version': '0.1',
    'depends': ['base', 'mrp', 'stock'],
    # always loaded
    'data': [
        'data/mrp_data.xml',
        # 'security/ir.model.access.csv',
        'views/mrp_production.xml',
        'views/stock_warehouse.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
#         'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
}
