# -*- coding: utf-8 -*-
from odoo import _
import odoo.http as http
from odoo.http import request
from odoo.addons.web.controllers.main import ExcelExport
from datetime import datetime
import json

class TableExporterXML(http.Controller):
    @http.route('/web/pivot/export_xml', type='http', auth="user")
    def export_xml(self, data, token):
        jdata = json.loads(data)
        headers = jdata['headers']
        rows = jdata['rows']
        jdata['measure_row']
        
class ExcelExportViewAccount(ExcelExport):
    def __getattribute__(self, name):
        if name == 'fmt':
            raise AttributeError()
        return super(ExcelExportViewAccount, self).__getattribute__(name)
    
    @http.route('/web/export/xls_txt_diot_download', type='http', auth='user')
    def export_account_xls_txt_view(self, token, **kw):
        record_ids = json.loads(kw.get('record_ids'))
        report_type = kw.get('report_type')
        lines = request.env['reporte.diot.wizard.line'].sudo().search([('id', 'in',record_ids)])
        rows = []
        tipo_proveedor_dict = dict([('04', _('04 - Proveedor nacional')),('05', _('05 - Proveedor extranjero')), ('15', _('15 - Proveedor global'))])
        tipo_operacion_dict = dict([('03', _('03 - Provisión de servicios profesionales')),('06', _('06 - Arrendamientos')), ('85', _('85 - Otros')),])
        for line in lines:
            data = [tipo_proveedor_dict.get(line.tipo_proveedor) or '',
                    tipo_operacion_dict.get(line.tipo_operacion) or '', 
                    line.rfc or '', 
                    line.registro_tributario or '', 
                    line.partner_id.name or '',
                    line.residencia_fiscal or '',
                    line.pagado_16_amount or 0,
                    line.pagado_16_amount_no_acreditable or 0,
                    line.pagado_8_amount or 0,
                    line.pagado_8_amount_no_acreditable or 0,
                    line.importacion_16 or 0,
                    line.pagado_0_amount or 0,
                    line.exento or 0,
                    ]
            if report_type=='txt':
                rows.append('|'.join(str(v) for v in data))
            else:
                rows.append(data)
        if report_type=='txt':
            content = '\n'.join(rows)
            filename = 'DIOT_%s.txt'%(datetime.today().strftime("%Y_%m_%d_%H_%M_%S"))
            content_type = 'text/csv;charset=utf8'
        else:
            columns_headers = ["Tipo de tercero", "Tipo de operacion","RFC", "No. ID fiscal", "Nombre", "Nacionalidad", 'Pagado 16%', 'Pagado 16% no acreditable', 'Pagado 8%', 'Pagado 8% no acreditable','Importacion 16%', 'Pagado 0%', 'Exento']
            filename = 'DIOT_%s.xls'%(datetime.today().strftime("%Y_%m_%d_%H_%M_%S"))
            content = self.from_data(columns_headers, rows)
            content_type = self.content_type
            
        return request.make_response(
            content,
            headers=[
                ('Content-Disposition', 'attachment; filename="%s"'
                 % filename),
                ('Content-Type', content_type)
            ],
            cookies={'fileToken': token}
        )
        
#     @http.route('/web/export/xls_account_view', type='http', auth='user')
#     def export_account_xls_view(self, token):
#         accounts = request.env['account.account'].sudo().search([])
#         rows = []
#         for account in accounts:
#             rows.append([account.code or '',account.c_agrupador or '', account.name or '', account.nivel or '', account.cuenta_tipo or ''])
#         
#         columns_headers = ["Código Odoo", "Código agrupador","Name", "Nivel", "Tipo Cuenta"]
#         filename = 'Accounts_%s.xls'%(datetime.today().strftime("%Y_%m_%d_%H_%M_%S"))
#         
#         return request.make_response(
#             self.from_data(columns_headers, rows),
#             headers=[
#                 ('Content-Disposition', 'attachment; filename="%s"'
#                  % filename),
#                 ('Content-Type', self.content_type)
#             ],
#             cookies={'fileToken': token}
#         )
        
    @http.route('/web/export/xml_account_view', type='http', auth='user')
    def export_account_xml_view(self, token):
        datas = request.env['account.account'].sudo().create_coa()
        filename = (request.env.user.company_id.factura_dir or '') + 'Accounts.xml'
        return request.make_response(
            datas,
            headers=[
                ('Content-Disposition', 'attachment; filename="%s"'
                 % filename),
                ('Content-Type', 'application/xml')
            ],
            cookies={'fileToken': token}
        )
        