# Copyright© 2022 ERP.M <http://www.erp-m.eu>

from odoo import models, fields, api, _


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model_create_multi
    def create(self, vals_list):
        new_recs = super(SaleOrder, self).create(vals_list)
        no_analytic_recs = new_recs.filtered(lambda n: not n.analytic_account_id)
        no_analytic_recs._create_analytic_account()
        return new_recs