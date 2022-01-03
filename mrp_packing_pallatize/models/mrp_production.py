
# -*- coding: utf-8 -*-

from odoo import models, exceptions, fields, api, _

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    picking_ids = fields.Many2many('stock.picking', string='Pickings', compute='_get_pickings')

    def _get_pickings(self):
        for mo in self:
            pickings = self.env['stock.picking'].search([('group_id', '=', mo.procurement_group_id.id)])
            mo.picking_ids = [(6, 0, pickings.ids)]