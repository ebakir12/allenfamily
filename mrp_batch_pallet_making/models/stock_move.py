# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools import float_compare, float_round, float_is_zero


class StockMove(models.Model):
    _inherit = 'stock.move'

    last_lot_id = fields.Many2one('stock.production.lot', 'Last Lot/Serial Number', store=True)
    workcenter_name = fields.Char('Workcenter', related='workorder_id.workcenter_id.name', readonly=True)

#     def _create_extra_move(self):
#         if self.procurement_id:
#             return super(StockMove, self)._create_extra_move()
#         else:
#             return self

    def action_merge_move_lots(self):
        # Merge the move lots, then do nothing.
        self.merge_move_lots()

        return {
            "type": "ir.actions.do_nothing",
        }

    def merge_move_lots(self):
        for move in self:
            if move.product_id.tracking != 'none':
                move_lots_without_produced_lot = move.mapped('active_move_lot_ids').filtered(lambda x: not x.lot_produced_id and x.quantity_done != 0)

                if move_lots_without_produced_lot:
                    produced_lot_id = move.mapped('active_move_lot_ids.lot_produced_id')

                    # TDE: TODO: Figure out why this gave false positive on MO/05474.
                    # if len(produced_lot_id) != 1:
                    #     # TODO: Test this error message.
                    #     raise UserError("You must specify a Finished Lot code on the Register Lots screen for: %s" % move.product_id.display_name)

                    for move_lot in move_lots_without_produced_lot:
                        move_lot.lot_produced_id = produced_lot_id[0]

                for movelot2merge in move.mapped('active_move_lot_ids'):
                    if not movelot2merge.exists():
                        continue
                    mergable_movelots = move.mapped('active_move_lot_ids').filtered(lambda x: x.lot_id == movelot2merge.lot_id and x.lot_produced_id == movelot2merge.lot_produced_id and x != movelot2merge)
                    movelot2merge.quantity_done += sum(mergable_movelots.mapped('quantity_done'))
                    mergable_movelots.unlink()
                    
                    