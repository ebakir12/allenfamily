# -*- coding: utf-8 -*-
{
    'name': 'Stock - Pickup Date',
    'version': '10.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'PPTS [India] Pvt.Ltd.',
    'website': 'https://www.pptssolutions.com',
    'category': 'Inventory',
    'depends': ['sale', 'sale_stock', 'stock', 'mrp'],
    'data': [
        'views/sale_order.xml',
        'views/stock_picking.xml',
    ],
    'installable': True,
    'application': True,
}