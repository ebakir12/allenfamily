# -*- coding: utf-8 -*-


from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_round
from odoo.addons import decimal_precision as dp


class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    gen_date = fields.Datetime('Date of Manufacture') # Legacy, no longer used. Use date_planned_start instead.

#     @api.multi
    def generate_final_lot_code(self):
        for wo in self:
            if wo.product_id.lot_abbv and '[USER_DEFINED' in wo.product_id.lot_abbv:
                return wo.action_view_generate_lot_wizard()
            else:
#                 gen_date = datetime.strptime(self.date_planned_start or fields.Datetime.now(), DEFAULT_SERVER_DATETIME_FORMAT)
                gen_date = self.date_planned_start or fields.Datetime.now()
                lot_name = wo.product_id.gen_lot_code(gen_date=gen_date)
                existing_lots = self.env['stock.production.lot'].search([('name', '=', lot_name), ('product_id', '=', wo.product_id.id)])

                if len(existing_lots.ids) > 0:
#                     wo.final_lot_id = existing_lots.ids[0]
                    wo.finished_lot_id = existing_lots.ids[0]
                else:
#                     wo.final_lot_id = wo.env['stock.production.lot'].create({
                    wo.finished_lot_id = wo.env['stock.production.lot'].create({
                        'name': lot_name,
                        'product_id': wo.product_id.id,
                        'gen_date': gen_date,
                    }).id
                    wo.finished_lot_id.sudo()._use_gen_date()
#                     wo.final_lot_id.sudo()._use_gen_date()
        return True

#     @api.multi
    def action_view_generate_lot_wizard(self):
        for wo in self:
#             imd = self.env['ir.model.data'].sudo()
#             action = imd.xmlid_to_object('product_auto_lot.action_view_generate_lot_code_wizard')
#             form_view_id = imd.xmlid_to_res_id('product_auto_lot.view_generate_lot_code_wizard')
# 
#             action.context = str({
#                 'default_workorder_id': wo.id,
#             })
# 
#             result = {
#                 'name': action.name,
#                 'help': action.help,
#                 'mode': action.type,
#                 'views': [[form_view_id, 'form']],
#                 'target': action.target,
#                 'context': action.context,
#                 'res_model': action.res_model,
#             }

            action = self.env.ref('product_auto_lot.action_view_generate_lot_code_wizard')
            form_view_id = self.env.ref('product_auto_lot.view_generate_lot_code_wizard').id
            context = dict(self.env.context or {})
            context['default_workorder_id'] = wo.id
    #         context['active_ids'] = [self.ids]
    #         context['active_model'] = 'mrp.production'
            result = {
                    'name': _(action.name),
                    'view_mode': 'form',
                    'res_model': action.res_model,
                    'view_id': form_view_id,
                    'type': 'ir.actions.act_window',
                    'context': context,
                    'target': 'new'
                }
    
            return result
        
        
        

#     @api.multi
    def print_lot_code(self):
        # for wo in self:
        return self.env['report'].get_action(self, 'product_auto_lot.report_mrp_workorder_lot_code_sheet')


