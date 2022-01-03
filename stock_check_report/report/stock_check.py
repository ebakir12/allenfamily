# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
import openerp.addons.decimal_precision as dp


class StockCheckReport(models.TransientModel):
    _name = 'report_stock_check_qweb'

    location = fields.Many2one(string='Location', comodel_name='stock.location')

    stock_check_ids = fields.One2many(
        comodel_name='report_stock_check_qweb_detail',
        inverse_name='report_id'
    )

class StockCheckReport(models.TransientModel):
    _name = 'report_stock_check_qweb_detail'

    report_id = fields.Many2one(
        comodel_name='report_stock_check_qweb',
        ondelete='cascade',
        index=True
    )

    loc = fields.Char(string='Loc')
    prod_name = fields.Char(string='Name')
    lot_code = fields.Char(string='Lot Code')
    quantity1 = fields.Float(string='Quantity',digits=(16, 2))
    uom = fields.Char(string='UOM')
    quantity2 = fields.Float(string='Quantity',digits=(16, 2))
    pack = fields.Char(string='Pack')


class StockCheckReportCompute(models.TransientModel):

    _inherit = 'report_stock_check_qweb'

    def get_report(self):
        self.ensure_one()
        report_name = 'stock_check_report.report_stock_check_qweb'
        data = self._get_report_values()
        return self.env['stock_check_report.report_stock_check_qweb'].report_action(self, data=data)

    def _get_report_values(self):
        self.ensure_one()
        return self._inject_stock_values()

    def _inject_stock_values(self):

        query_inject = """
        WITH
            stock_details AS (
            SELECT
                loc.name AS loc, 
                CASE
                    WHEN tmpl.default_code is null then tmpl.name
                    ELSE '[' || tmpl.default_code ||'] ' || tmpl.name 
                END AS prod_name, 
                lot.name AS lot_code, 
                stock.total AS quantity1, 
                uom.name AS uom,
                CASE
					WHEN uom.name=po_uom.name then stock.total
                    ELSE stock.total * po_uom.factor / uom.factor
                END AS quantity2, 
                po_uom.name AS pack
            FROM (
                SELECT location_id, lot_id, product_id, sum(quantity) AS total FROM stock_quant GROUP BY location_id, lot_id, product_id
                having sum(quantity) != 0
            ) stock
            JOIN product_product product ON stock.product_id=product.id
            JOIN product_template tmpl ON product.product_tmpl_id = tmpl.id
            JOIN stock_location loc ON stock.location_id = loc.id
            LEFT JOIN stock_production_lot lot ON stock.lot_id = lot.id
            JOIN uom_uom uom ON tmpl.uom_id = uom.id
            LEFT JOIN uom_uom po_uom ON tmpl.uom_packaged_id = po_uom.id
            WHERE stock.location_id IN (select id from stock_location WHERE location_id = %(location)s  or id = %(location)s )
            AND tmpl.name != '' AND tmpl.type = 'product'
            ORDER BY loc.complete_name, tmpl.default_code, tmpl.name, lot.name
            )
            """

        query_inject += """
            INSERT INTO report_stock_check_qweb_detail
            (
                report_id,
                create_uid,
                create_date,
                loc,
                prod_name,
                lot_code,
                quantity1,
                uom,
                quantity2,
                pack
            )
            SELECT
                %(report_id)s AS report_id,
                %(create_uid)s AS create_uid,
                NOW() AS create_date,
                loc,
                prod_name,
                lot_code,
                quantity1,
                uom,
                quantity2,
                pack
            FROM
                stock_details
        """

        query_inject_params = {
            'report_id': self.id,
            'create_uid': self.env.uid,
            'location': self.location.id
        }

        return self.env.cr.execute(query_inject, query_inject_params)