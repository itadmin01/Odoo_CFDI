# -*- coding: utf-8 -*-
##############################################################################
#                 @author Esousy
#
##############################################################################

{
    'name': 'Punto de Venta Factura Electronica Mexico CFDI',
    'version': '9.0',
    'description': ''' Punto de Venta Factura Electronica Mexico (CFDI 3.3).
    ''',
    'category': 'Sales, Point Of Sale, Accounting',
    'author': 'IT Admin',
    'website': '',
    'depends': [
        'base',
        'point_of_sale',
        'sale','account'
    ],
    'data': [
        'views/res_partner_view.xml',
        'views/res_company_view.xml',
        'views/product_view.xml',
        'views/account_invoice_view.xml',
        'views/account_payment_view.xml',
        'views/account_tax_view.xml',
        'views/point_of_sale_view.xml',
        'views/sale_view.xml',
        'wizard/create_invoice_wizard.xml',
        'wizard/create_invoice_total_wizard.xml',
        'wizard/create_invoice_session_wizard.xml',
        'report/invoice_report.xml',
        'report/payment_report.xml',
        'report/sale_report_templates.xml',
        'data/mail_template_data.xml',
        'data/factura_global.xml',
	],
    'qweb': [
        'static/src/xml/pos.xml',
    ],
    'application': False,
    'installable': True,
    'price': 0.00,
    'currency': 'USD',
}
