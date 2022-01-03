# -*- coding: utf-8 -*-
# Author: Damien Crier
# Author: Julien Coux
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api

class StockCheckReportWizard(models.TransientModel):
    """Inventory check report wizard."""

    _name = "stock.check.report.wizard"
    _description = "Stock Check Report Wizard"

    loc_ids1 = fields.Many2one(
        'stock.location', 'Warehouse',
        auto_join=True, index=True, required=True,
        help="Warehouse where the system will stock the finished products.")

    loc_ids2 = fields.Many2one(
        'stock.location', 'Location',
        auto_join=True, index=True, required=True,
        help="Location where the system will stock the finished products.")

    def button_export_pdf(self):
        self.ensure_one()
        return self._export()

    def _prepare_stock_check_report(self):
        self.ensure_one()
        return {
            'location': self.loc_ids2.id
        }

    def _export(self):
        model = self.env['report_stock_check_qweb']
        report_to_create = self._prepare_stock_check_report()
        report = model.create(report_to_create)
        return self.env.ref('stock_check_report.action_report_stock_check_qweb').report_action(self, report_to_create)
