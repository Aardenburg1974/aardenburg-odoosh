# Copyright© 2022 ERP.M <http://www.erp-m.eu>

from odoo import models, fields, api, _


class ProductTemplate(models.Model):
    _inherit = "product.template"

    agro_analytic_plan_id = fields.Many2one(
        comodel_name='account.analytic.plan',compute='_compute_agro_analytic_plan',
        inverse='_set_agro_analytic_plan', store=True)

    @api.depends('product_variant_ids', 'product_variant_ids.agro_analytic_plan_id')
    def _compute_agro_analytic_plan(self):
        unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1 and template.product_variant_ids.agro_analytic_plan_id)
        for template in unique_variants:
            template.agro_analytic_plan_id = template.product_variant_ids.agro_analytic_plan_id.id
        for template in (self - unique_variants):
            template.agro_analytic_plan_id = False

    def _set_agro_analytic_plan(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.agro_analytic_plan_id = template.agro_analytic_plan_id and template.agro_analytic_plan_id.id or False