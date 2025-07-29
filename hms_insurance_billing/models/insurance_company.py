from odoo import models, fields, api
from odoo.exceptions import ValidationError


class InsuranceCompany(models.Model):
    _name = 'insurance.company'
    _description = 'Insurance Company'

    name = fields.Char(string="Company Name", required=True)
    coverage_percentage = fields.Float(string="Coverage Percentage", required=True)

    @api.constrains('coverage_percentage')
    def _check_coverage_percentage(self):
        for record in self:
            if record.coverage_percentage < 0 or record.coverage_percentage > 100:
                raise ValidationError("Coverage percentage must be between 0 and 100.")
