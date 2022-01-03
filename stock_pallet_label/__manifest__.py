# -*- coding: utf-8 -*-
{
    'name': 'Pallet Label Sticker',
    'version': '14.0.0.0.0',
    'category': 'Reporting',
    'summary': 'Inventory Check Reports',
    'author': 'James chung',
    'depends': [
        'stock'
    ],
    'data': [
        'reports/stock_picking.xml',
        'reports/report_paperformat_data.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'AGPL-3',
}
