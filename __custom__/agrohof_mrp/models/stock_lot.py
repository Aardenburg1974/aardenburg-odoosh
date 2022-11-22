# Copyright© 2022 ERP.M <http://www.erp-m.eu>

from odoo import models, fields, api, _


class StockLot(models.Model):
    _inherit = "stock.lot"

    # @api.model
    # def generate_lot_names(self, first_lot, count):
    #     """Generate `lot_names` from a string."""
    #     # We look if the first lot contains at least one digit.
    #     caught_initial_number = regex_findall(r"\d+", first_lot)
    #     if not caught_initial_number:
    #         return self.generate_lot_names(first_lot + "0", count)
    #     # We base the series on the last number found in the base lot.
    #     initial_number = caught_initial_number[-1]
    #     padding = len(initial_number)
    #     # We split the lot name to get the prefix and suffix.
    #     splitted = regex_split(initial_number, first_lot)
    #     # initial_number could appear several times, e.g. BAV023B00001S00001
    #     prefix = initial_number.join(splitted[:-1])
    #     suffix = splitted[-1]
    #     initial_number = int(initial_number)

    #     lot_names = []
    #     for i in range(0, count):
    #         lot_names.append('%s%s%s' % (
    #             prefix,
    #             str(initial_number + i).zfill(padding),
    #             suffix
    #         ))
    #     return lot_names

    @api.model
    def _get_next_serial(self, company, product):
        if product.tracking == "serial" and product.default_code and product.agro_analytic_plan_id:
            last_serial = self.env['stock.lot'].search(
                [('company_id', '=', company.id), ('name', 'like', product.default_code)],
                limit=1, order='name DESC')
            if last_serial:
                return self.env['stock.lot'].generate_lot_names(last_serial.name, 3)[1]
            else:
                return "%s001" % product.default_code
        return super(StockLot, self)._get_next_serial(company, product)
