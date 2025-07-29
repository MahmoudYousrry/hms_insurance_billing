from odoo import models, api, fields
from odoo.exceptions import ValidationError

class InsuranceInvoiceHandler(models.Model):
    _inherit = 'account.move'


    def action_post(self):
        res = super().action_post()

        for invoice in self:
            partner = invoice.partner_id
            insurance_company = partner.insurance_company_id

            if insurance_company and invoice.move_type == 'out_invoice':
                coverage_percentage = insurance_company.coverage_percentage or 0.0
                if coverage_percentage <= 0:
                    continue  

                total_amount = invoice.amount_total
                insurance_amount = total_amount * (coverage_percentage / 100.0)

                if insurance_amount <= 0:
                    continue
                    
                payment = self.env['account.payment'].create({
                    'partner_id': partner.id,
                    'amount': insurance_amount,
                    'payment_type': 'inbound',
                    'partner_type': 'customer',
                    'journal_id': self.env['account.journal'].search([('type', '=', 'cash')], limit=1).id,
                })
                payment.action_post()

        return res
