# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplateRateAndSKU(models.Model):
    _inherit = 'product.template'

    uom_packaged_id = fields.Many2one(string='Packaged Unit of Measure', comodel_name='uom.uom', required=False)

    # Check if the selected uom_packaged_id is of the same category to prevent conversion errors.
    @api.onchange('uom_packaged_id')
    def _onchange_uom_packaged(self):
        if self.uom_id and self.uom_packaged_id and self.uom_id.category_id != self.uom_packaged_id.category_id:
            # If category of selected UOM doesn't match, fall back and set to default UOM of product.
            self.uom_packaged_id = self.uom_id

