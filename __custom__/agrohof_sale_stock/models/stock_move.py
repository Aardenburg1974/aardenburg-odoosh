# Copyright© 2022 ERP.M <http://www.erp-m.eu>

from odoo import models, fields, api, _


class StockMove(models.Model):
    _inherit = "stock.move"

    def write(self, vals):
        # Before write
        ret = super().write(vals)
        # After write
        for rec in self.filtered(lambda sm: sm.lot_ids and sm.sale_line_id):
            serial_numbers = rec.mapped('lot_ids.name')
            sn_analytic_account = self.env['account.analytic.account'].sudo().search([('name', 'in', serial_numbers)], limit=1)
            if sn_analytic_account:
                analytic_distribution = rec.sale_line_id.analytic_distribution or {}
                analytic_distribution.update({str(sn_analytic_account.id): 100.00})
                rec.sale_line_id.analytic_distribution = analytic_distribution
        return ret