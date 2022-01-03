# -*- coding: utf-8 -*-

from odoo import models, fields


class StockOnHandUOM(models.Model):
    _inherit = 'stock.quant'

    uom_packaged_id = fields.Char('Packaged Unit', compute='compute_uom_value', readonly=True)

    def compute_uom_value(self):
        for rec in self:
            if rec.product_id.uom_packaged_id:
                rec.uom_packaged_id = str(rec.product_uom_id._compute_quantity(rec.qty, rec.product_id.uom_packaged_id)) \
                          + ' ' + str(rec.product_id.uom_packaged_id.name)
            else:
                rec.uom_packaged_id = str(rec.product_uom_id._compute_quantity(rec.qty, rec.product_id.uom_id)) \
                          + ' ' + str(rec.product_id.uom_id.name)

