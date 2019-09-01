# -*- coding: utf-8 -*-
##############################################################################
#                 @author IT Admin
#
##############################################################################

{
    'name': 'Contabildad Electronica Mexico',
    'version': '1.0',
    'description': ''' Contabilidad Electronica para Mexico (CFDI 1.3)
    ''',
    'category': 'Accounting',
    'author': 'IT Admin',
    'website': 'www.itadmin.com.mx',
    'depends': [
        'base',
        'account',
        'account_invoicing',
        'date_range',
        'report_xlsx',
        'cdfi_invoice',
    ],
    'data': [
        'views/menu.xml',
        'data/res_currency_data.xml',
        'wizard/trial_balance_wizard_view.xml',
        'menuitems.xml',
        'reports.xml',
        'report/templates/layouts.xml',
        'report/templates/trial_balance.xml',
        'report/templates/account_hirarchy.xml',
        'views/account_account_view.xml',
        'views/account_group.xml',
        'views/res_partner_view.xml',
        'views/res_currency_views.xml',
        'views/report_trial_balance.xml',
        'views/report_template.xml',
        'views/account_move.xml',
        'views/templates.xml',
        "wizard/generar_xml_hirarchy.xml",
        "wizard/polizas_report_view.xml",
        "wizard/reporte_diot.xml",
        'wizard/actualizar_polizas_view.xml',
    ],
    'application': False,
    'installable': True,
    'price': 0.00,
    'currency': 'USD',
    'license': 'OPL-1',
}
