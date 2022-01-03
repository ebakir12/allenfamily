# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class StockPicking(models.Model):
    _inherit = "stock.picking"

    stock_pickup_date = fields.Datetime('Pickup Date',
                                help="Pickup date of all deliveries bound for customer. ",
                                store=True,
                                inverse = '_set_pickup')

    def _set_pickup(self):
        sale_order = self.sale_id

        if sale_order.pickup_date != self.stock_pickup_date:
            sale_order.write({'pickup_date': self.stock_pickup_date})

        if self.move_lines:
            for move in self.move_lines.filtered(lambda x: x.state not in ['done', 'cancel']):
                move.write({'stock_pickup_date': self.stock_pickup_date})

