# -*- coding: utf-8 -*-

{
    'name': 'Stock - Add package Unit of measurement',
    'version': '14.0.1.0.0',
    'license': 'AGPL-3',
    'author': "David Hong, James Chung",
    'category': 'Inventory',
    'depends': ['stock', 'mrp'],
    'data': [
        'views/stock_quant_package_uom.xml',
        'views/product_temp_add_edit_sku_rate.xml',
    ],
    'installable': True,
}
