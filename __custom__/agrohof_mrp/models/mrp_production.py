# Copyright© 2022 ERP.M <http://www.erp-m.eu>

from odoo import models, fields, api, _


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    analytic_account_id = fields.Many2one(
        'account.analytic.account', 'Analytic Account', copy=True,
        help="Analytic account in which cost and revenue entries will take\
        place for financial management of the manufacturing order.",
        compute='_compute_analytic_account_id', store=True, readonly=False)

    @api.depends('lot_producing_id')
    def _compute_analytic_account_id(self):
        for rec in self:
            if rec.lot_producing_id and rec.product_id.agro_analytic_plan_id:
                rec.analytic_account_id = rec._get_or_create_analytic_account()

    def _prepare_analytic_account_data(self):
        self.ensure_one()
        name = self.lot_producing_id.name
        plan = self.product_id.agro_analytic_plan_id
        if not plan:
            plan = self.env['account.analytic.plan'].create({
                'name': 'Default',
                'company_id': self.company_id.id,
            })
        return {
            'name': name,
            'code': name,
            'company_id': self.company_id.id,
            'plan_id': plan.id
        }

    def _get_or_create_analytic_account(self):
        analytic = self.env['account.analytic.account'].search([
            ('name', '=', self.lot_producing_id.name),
            '|',
            ('company_id', '=', self.company_id.id), ('company_id', '=', False)], limit=1)
        if not analytic:
            analytic = self.env['account.analytic.account'].create(self._prepare_analytic_account_data())
        return analytic
            
    def action_confirm(self):
        for rec in self:
            if rec.product_id.tracking == 'serial':
                rec.action_generate_serial()
        return super(MrpProduction, self).action_confirm()
        




