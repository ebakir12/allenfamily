# -*- coding: utf-8 -*-
{
    "name": "Manufacturing - Workorder Multi Lot",
    "version": "14.0.1.0.0",
    "category": "Manufacturing",
    "license": "AGPL-3",
    'author': 'PPTS [India] Pvt.Ltd.',
    'website': 'https://www.pptssolutions.com',
    "contributors": [
    ],
    "depends": [
        'base',
        'mrp',
        'stock',
#         'web_widget_many2many_tags_multi_selection',
    ],
    "data": [
        # "data/mrp_data.xml",
        "views/mrp_workorder.xml",
        "views/stock_production_lot.xml"
        # "views/stock_warehouse.xml",
    ],
    "installable": True,
    'application': True,
}

# Note by jana
# This app cannot be converted to odoo14
# - There is no options to select lots on workorders.
# - and table which is used to load lot values not preast in odoo14.
# - Lots can be selected on MRP order itself.
