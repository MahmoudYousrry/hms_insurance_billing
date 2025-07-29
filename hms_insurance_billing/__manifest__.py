{
    'name': 'Insurance Billing',
    'version': '1.0',
    'depends': ['base', 'account'],
    'summary': 'Standalone module for patient invoicing and insurance-covered payments',
    'data': [
        'security/ir.model.access.csv',
        'views/billing_invoice_action.xml',
        'views/insurance_company_views.xml',
    ],
    'installable': True,
    'application': False,
}
