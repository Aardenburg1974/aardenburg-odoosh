# Copyright© 2022 ERP.M <http://www.erp-m.eu>

from odoo import models, fields, api, _


class ProductProduct(models.Model):
    _inherit = "product.product"

    agro_analytic_plan_id = fields.Many2one(
        comodel_name='account.analytic.plan')
