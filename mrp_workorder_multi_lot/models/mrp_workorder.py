# -*- coding: utf-8 -*-

from odoo import api, exceptions, fields, models, _
from odoo.addons import decimal_precision as dp


class MrpProduction(models.Model):
    _inherit = 'mrp.workorder'

    # Convert field to many2many field. Allows multiple selection
    # Requires web_widget_many2many_tags_multi_selection from web repo
    select_lot_ids = fields.Many2many('stock.production.lot', string='Select Lot Codes', store=False, create_edit=False, help='Select a lot code to add to this workorder.')

    raw_product_ids = fields.Many2many('product.product', compute='_raw_product_ids')

    @api.returns('stock.production.lot')
    def _get_top_three_lot_ids(self, product_id):
        self.ensure_one()
        stock_production_lot = self.env['stock.production.lot']

        # Get all the child locations of the source location.
        child_locations = self.env['stock.location'].search([('location_id', 'child_of', self.production_id.location_src_id.id)])

        # Get the lots that have quants at our child locations.
        lot_ids = stock_production_lot.search(
            [('product_id', '=', product_id), ('quant_ids.location_id', 'in', child_locations.ids)])

        # Filter out lots with negative or zero quantity.
        # Sort the lots by the qty available at the locations.
        # TODO: This should be done in a FEFO/FIFO way based on product category.
        sorted_lot_ids = lot_ids.filtered(lambda x: sum(x.mapped('quant_ids').filtered(
            lambda s: bool(set(s.mapped('location_id').ids) & set(child_locations.ids))).mapped('quantity')) >= 0) \
            .sorted(lambda x: sum(x.mapped('quant_ids').filtered(
            lambda s: bool(set(s.mapped('location_id').ids) & set(child_locations.ids))).mapped('quantity')), reverse=True)

        # Return only the top 3.
        return sorted_lot_ids[:3]

#     def button_auto_select_lots(self):
#         for wo in self:
#             for raw_product in wo.move_line_ids.mapped('product_id'):
#                 sorted_lots = wo._get_top_three_lot_ids(raw_product.id)
#                 for lot in sorted_lots:
#                     active_moves = wo.move_line_ids.filtered(
#                         lambda x: x.product_id.id == lot.product_id.id)
#                     if active_moves:
#                         blank_move_lot = active_moves.filtered(lambda m: not m.lot_id and m.product_id.id == lot.product_id.id)
#                         move_lots = active_moves.filtered(lambda m: m.lot_id.id == lot.id)
# 
#                         child_location = wo.env['stock.location'].search(
#                             [('location_id', 'child_of', wo.production_id.location_src_id.id)])
# 
#                         quantity_at_location = sum(lot.mapped('quant_ids').filtered(
#                             lambda x: bool(set(x.mapped('location_id').ids) & set(child_location.ids))).mapped('quantity'))
# 
#                         # TODO: Should we use the unreserved quantity?
#                         # qty_unreserved = sum(lot.mapped('quant_ids').filtered(
#                         #     lambda x: bool(set(x.mapped('location_id').ids) & set(
#                         #         child_location.ids)) and not x.reservation_id).mapped('qty'))
#                         # qty_all = sum(lot.mapped('quant_ids').filtered(
#                         #     lambda x: bool(set(x.mapped('location_id').ids) & set(child_location.ids))).mapped('qty'))
# 
#                         # Get the remaining quantity to do.
#                         quantity_done = active_moves.filtered(lambda m: m.lot_id.id).mapped('quantity_done')
#                         quantity = active_moves.mapped('quantity')
#                         quantity_todo = sum(quantity) - sum(quantity_done)
#                         if move_lots:
#                             continue
#                         elif blank_move_lot:
#                             blank_move_lot[0].lot_id = lot.id
#                             blank_move_lot[0].quantity_done = max(min(quantity_at_location, quantity_todo), 0)
#                         else:
#                             if quantity_todo:
#                                 wo.move_line_ids.create({'move_id': active_moves[0].move_id.id,
#                                                               'lot_id': lot.id,
#                                                               'quantity_done': max(min(quantity_at_location, quantity_todo), 0),
#                                                               'quantity': 0.0,
#                                                               'workorder_id': wo.id,
#                                                               'production_id': wo.production_id.id,
#                                                               'product_id': lot.product_id.id,
#                                                               'done_wo': False})

    def _raw_product_ids(self):
        for rec in self:
#             for raw in rec.production_id.move_raw_ids:
#                 print(raw.workorder_id)
            product_ids = rec.production_id.move_raw_ids.filtered(lambda x: x.workorder_id.id == rec.id).mapped('product_id')
#             product_ids = rec.move_line_ids.mapped('product_id')
            rec.raw_product_ids = [(4, x.id) for x in product_ids]

    @api.onchange('select_lot_ids')
    def _select_lot(self):
        if self.select_lot_ids:
            lot_ids = self.select_lot_ids.filtered(lambda x: x._origin not in self.production_id.move_raw_ids.mapped('move_line_ids').mapped('lot_id'))
#             lot_ids = self.select_lot_ids.filtered(lambda x: x not in self.move_line_ids.mapped('lot_id'))
 
            for lot in lot_ids:
                active_moves = self.production_id.move_raw_ids.mapped('move_line_ids').filtered(lambda x: x.product_id.id == lot.product_id.id)
#                 active_moves = self.move_line_ids.filtered(lambda x: x.product_id.id == lot.product_id.id)
                if not active_moves:
                    move_raw = self.production_id.move_raw_ids.filtered(lambda x: x.product_id.id == lot.product_id.id)
                if active_moves:
                    blank_move_lot = active_moves.filtered(lambda m: not m.lot_id)
                    move_lots = active_moves.filtered(lambda m: m.lot_id.id == lot._origin.id)
                    child_location = self.env['stock.location'].search([('location_id', 'child_of', self.production_id.location_src_id.id)])
                    quantity_at_location = sum(lot.mapped('quant_ids').filtered(lambda x: bool(set(x.mapped('location_id').ids) & set(child_location.ids))).mapped('quantity'))
                    # Get the remaining quantity to do.
                    quantity_done = active_moves.filtered(lambda m: m.lot_id.id).mapped('qty_done')
                    quantity = active_moves.mapped('product_uom_qty')
                    quantity_todo = sum(quantity) - sum(quantity_done)
                    if move_lots:
 
                        return
                    elif blank_move_lot:
                        blank_move_lot[0].lot_id = lot._origin.id
                        blank_move_lot._origin[0].qty_done = max(min(quantity_at_location, quantity_todo), 0)
                    else:
                        location_dest_id = active_moves[0].move_id.location_dest_id._get_putaway_strategy(lot.product_id).id or active_moves[0].move_id.location_dest_id.id
                        self.move_line_ids.create({'move_id': active_moves[0].move_id.id,
                                                      'lot_id': lot._origin.id,
#                                                       'quantity_done': max(min(quantity_at_location, quantity_todo), 0),
                                                      'qty_done': max(min(quantity_at_location, quantity_todo), 0),
                                                      'product_uom_qty': 0.0,
                                                      'workorder_id': self._origin.id,
                                                      'production_id': self.production_id.id,
                                                      'location_id': active_moves[0].move_id.location_id.id,
                                                      'location_dest_id': location_dest_id,
                                                      'product_uom_id': lot.product_id.uom_id.id,
                                                      'product_id': lot.product_id.id})
#                                                       'done_wo': False})
                elif move_raw:
                    # If the move lot is missing or was deleted, we can create a new one.
                    child_location = self.env['stock.location'].search([('location_id', 'child_of', self.production_id.location_src_id.id)])
 
                    quantity_at_location = sum(lot.mapped('quant_ids').filtered(lambda x: bool(set(x.mapped('location_id').ids) & set(child_location.ids))).mapped('quantity'))
                    quantity_todo = move_raw.unit_factor * self.qty_producing
#                     location_ids = lot.mapped('quant_ids').mapped('location_id')
                    location_dest_id = move_raw.location_dest_id._get_putaway_strategy(lot.product_id).id or move_raw.location_dest_id.id
                    self.production_id.move_raw_ids.move_line_ids.create({'move_id': move_raw.id,
                                                  'lot_id': lot._origin.id,
                                                  'qty_done': max(min(quantity_at_location, quantity_todo), 0),
                                                  'product_uom_id': lot.product_id.uom_id.id,
                                                  'product_uom_qty': quantity_todo,
                                                  'workorder_id': self._origin.id,
                                                  'production_id': self.production_id.id,
#                                                   'location_id':location_ids and location_ids[0].id,
                                                  'location_id': move_raw.location_id.id,
                                                  'location_dest_id': location_dest_id,
                                                  'product_id': lot.product_id.id})
#                                                   'done_wo': False})

#                     self.move_line_ids.new({'move_id': move_raw.id,
#                                                   'lot_id': lot._origin.id,
#                                                   'qty_done': max(min(quantity_at_location, quantity_todo), 0),
# #                                                   'quantity_done': max(min(quantity_at_location, quantity_todo), 0),
#                                                   'product_uom_qty': quantity_todo,
#                                                   'workorder_id': self._originid,
#                                                   'production_id': self.production_id.id,
#                                                   'product_id': lot.product_id.id})
#                                                   'done_wo': False})


