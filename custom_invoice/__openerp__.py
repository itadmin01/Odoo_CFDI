# -*- coding: utf-8 -*-
##############################################################################
#                 @author Esousy
#
##############################################################################

{
    'name': 'Mexican Invoice',
    'version': '9.0',
    'description': ''' Mexican Invoice.
    ''',
    'category': 'Sales, Point Of Sale, Accounting',
    'author': 'Esousy',
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
        'views/point_of_sale_view.xml',
        #'views/sale.xml',
        'wizard/create_invoice_wizard.xml',
        'wizard/create_invoice_total_wizard.xml',
        'report/invoice_report.xml',
    ],
    'qweb': [
        'static/src/xml/pos.xml',
    ],
    'application': False,
    'installable': True,
}
