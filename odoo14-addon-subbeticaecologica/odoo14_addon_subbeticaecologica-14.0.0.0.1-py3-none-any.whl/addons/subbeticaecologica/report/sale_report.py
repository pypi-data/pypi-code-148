from odoo import fields, models


class SaleReport(models.Model):
    _inherit = "sale.report"

    carrier_name = fields.Char('Delivery method', readonly=True)

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['carrier_name'] = ", carrier.name as carrier_name"
        groupby += ', carrier.name'

        from_clause += "join delivery_carrier carrier on s.carrier_id = carrier.id"

        return super(SaleReport, self)._query(with_clause, fields, groupby, from_clause)
