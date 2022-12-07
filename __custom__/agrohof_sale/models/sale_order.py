# Copyright© 2022 ERP.M <http://www.erp-m.eu>

from odoo import models, fields, api, _


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model
    def create(self, vals):
        rec = super(SaleOrder, self).create(vals)
        if rec and not rec.analytic_account_id:
            rec._create_analytic_account()
        return rec