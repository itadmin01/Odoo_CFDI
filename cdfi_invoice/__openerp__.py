# -*- coding: utf-8 -*-
##############################################################################
#                 @author Esousy
#
##############################################################################

{
    'name': 'Ventas Factura Electronica Mexico CFDI',
    'version': '9.0',
    'description': ''' Factura Electronica módulo de ventas para Mexico (CFDI 2017)
    ''',
    'category': 'Sales, Accounting',
    'author': 'IT Admin',
    'website': '',
    'depends': [
        'base',
        'sale','account'
    ],
    'data': [
        'views/res_partner_view.xml',
        'views/res_company_view.xml',
        'views/product_view.xml',
        'views/account_invoice_view.xml',
        'views/account_payment_view.xml',
        'views/account_tax_view.xml',
        'views/sale_view.xml',
        'report/invoice_report.xml',
        'report/payment_report.xml',
        'report/sale_report_templates.xml',
        'data/mail_template_data.xml',
    ],
    'application': False,
    'installable': True,
    'price': 0.00,
    'currency': 'USD',
}
