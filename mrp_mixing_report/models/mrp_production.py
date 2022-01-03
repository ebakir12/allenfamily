# -*- coding: utf-8 -*-
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, exceptions, fields, models, _
from odoo.addons import decimal_precision as dp
import math

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    totalpage = fields.Integer('TotalPage', compute='_cal_total_page')

    def _cal_total_page(self):
        PalletPerPage = 25
        self.totalpage = math.ceil(self.product_qty / PalletPerPage)

    # This will grab the top 3 lots with quantity at the production order's raw material warehouse location.
    def _get_top_three_lot_ids(self, product_id):
        self.ensure_one()
        stock_production_lot = self.env['stock.production.lot']

        # Get all the child locations of the source location.
        child_locations = self.env['stock.location'].search([('location_id', 'child_of', self.location_src_id.id)])

        # Get the lots that have quants at our child locations.
        lot_ids = stock_production_lot.search([('product_id', '=', product_id), ('quant_ids.location_id', 'in', child_locations.ids)])

        # Filter out lots with negative or zero quantity.
        # Sort the lots by the qty available at the locations.
        sorted_lot_ids = lot_ids.filtered(lambda x: sum(x.mapped('quant_ids').filtered(lambda s: bool(set(s.mapped('location_id').ids) & set(child_locations.ids))).mapped('quantity')) >= 0)\
            .sorted(lambda x: sum(x.mapped('quant_ids').filtered(lambda s: bool(set(s.mapped('location_id').ids) & set(child_locations.ids))).mapped('quantity')), reverse=True)

        # Return only the top 3.
        return sorted_lot_ids[:3]
