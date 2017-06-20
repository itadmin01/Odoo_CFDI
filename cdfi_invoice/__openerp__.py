# -*- coding: utf-8 -*-
##############################################################################
#                 @author Esousy
#
##############################################################################

{
    'name': 'CDFI Invoice',
    'version': '9.0',
    'description': ''' CDFI Mexican Invoice.
    ''',
    'category': 'Sales, Accounting',
    'author': 'Esousy',
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
        # 'views/sale.xml',
        'report/invoice_report.xml',
    ],
    'application': False,
    'installable': True,
}
