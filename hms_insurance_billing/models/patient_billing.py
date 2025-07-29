from odoo import models, api
from odoo.exceptions import ValidationError

class BillingService(models.AbstractModel):
    _name = 'hms.billing.service'
    _description = 'Service to Handle Invoice Logic'

    @api.model
    def create_or_get_invoice(self, patient_name, national_id):
        if not national_id:
            raise ValidationError("National ID is required to bill the patient.")

        partner = self.env['res.partner'].search([('national_id', '=', national_id)], limit=1)
        if not partner:
            raise ValidationError("This patient is not registered. Please register them first.")

        invoice = self.env['account.move'].search([
            ('partner_id', '=', partner.id),
            ('state', '=', 'draft'),
            ('move_type', '=', 'out_invoice'),
        ], limit=1)

        if not invoice:
            invoice = self.env['account.move'].create({
                'move_type': 'out_invoice',
                'partner_id': partner.id,
            })

        return invoice

    @api.model
    def add_invoice_line(self, invoice, lines):
        new_lines = []
        for line in lines:
            price = line.get('price_unit', 0)
            if price < 0:
                raise ValidationError("Invalid amount in line")

            quantity = line.get('quantity', 1.0)
            new_lines.append((0, 0, {
                'name': line.get('name') or 'Service',
                'quantity': quantity,
                'price_unit': price,
            }))
        invoice.write({'invoice_line_ids': new_lines})

    @api.model
    def bill_static_item(self, patient_name, national_id, description, amount):
        invoice = self.create_or_get_invoice(patient_name, national_id)
        self.add_invoice_line(invoice, [{
            'name': description,
            'price_unit': amount,
        }])

    @api.model
    def bill_dynamic_lines(self, patient_name, national_id, record, line_name):
        invoice_line_data = {
            'name': line_name,
            'price_unit': record.price,
            'quantity': getattr(record, 'quantity', 1.0)
        }
        invoice = self.create_or_get_invoice(patient_name, national_id)
        self.add_invoice_line(invoice, [invoice_line_data])

    @api.model
    def bill_item(self, *, patient_name=None, national_id=None, description=None, amount=None, lines=None, record=None, line_name=None):
        """
        Route billing to the correct method based on input.
        """
        if record:
            return self.bill_dynamic_lines(patient_name, national_id, record, line_name)
        elif description and amount is not None:
            return self.bill_static_item(patient_name, national_id, description, amount)
