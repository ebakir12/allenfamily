# -*- coding: utf-8 -*-
{
    'name': 'Inventory Check Report',
    'version': '14.0.0.0.0',
    'category': 'Reporting',
    'summary': 'Inventory Check Reports',
    'author': 'John Lee, James chung',
    'depends': [
        'stock'
    ],
    'data': [
        'menuitems.xml',
        'wizard/stock_check_report_wizard_view.xml',
        'report/stock_check.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'AGPL-3',
}
