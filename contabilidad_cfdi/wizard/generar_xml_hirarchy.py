
from odoo import api, models, fields,_
import requests
from odoo.exceptions import UserError
from datetime import datetime
import base64
import json
import logging
_logger = logging.getLogger(__name__)

class GenerarXmlHirarchyWizard(models.TransientModel):
    _name = 'generar.xml.hirarchy.wizard'
    
    fecha_mes = fields.Selection([(1, 'Enero'), (2, 'Febrero'), (3, 'Marzo'), (4, 'Abril'), (5, 'Mayo'), (6, 'Junio'),
                                    (7, 'Julio'), (8, 'Agosto'), (9, 'Septiembre'), (10, 'Octubre'), (11, 'Noviembre'), (12, 'Diciembre')],
                                   string='Mes')
    fecha_ano = fields.Selection([(2018, '2018'), (2019, '2019')],
                                   string='Año')
    procesa_nivel = fields.Char(string='Nivel a procesar',store=True,default='2')
    tipo_de_reporte = fields.Selection([('Catalogo de cuentas','Catalogo de cuentas'),('Balance mensual', 'Balance mensual')],string='Tipo de reporte')
    
    @api.model
    def default_get(self, fields_list):
        res = super(GenerarXmlHirarchyWizard, self).default_get(fields_list)
        ctx = self._context.copy()
        if ctx.get('is_account_hirarchy_report'):
            res['tipo_de_reporte'] = 'Catalogo de cuentas'
        else:
            res['tipo_de_reporte'] = 'Balance mensual'
        if ctx.get('default_fecha_mes'):
            try:
                res['fecha_mes'] = int(ctx.get('default_fecha_mes'))
            except Exception:
                pass
        if ctx.get('default_fecha_ano'):
            try:
                res['fecha_ano'] = int(ctx.get('default_fecha_ano'))
            except Exception:
                pass
        return res
    
    @api.model
    def to_json(self, report):
        company = self.env.user.company_id
        request_params = { 
                'company': {
                      'rfc': company.rfc,
                      'api_key': company.proveedor_timbrado,
                      'modo_prueba': company.modo_prueba,
                },}
        account_lines = []
        account_obj = self.env['account.account']
        if self.tipo_de_reporte == 'Catalogo de cuentas':
            request_params.update({'informacion':{
                      'proceso': 'catalogo_cuentas',
                      'fecha_mes': self.fecha_mes,
                      'fecha_ano': self.fecha_ano,
                      'procesa_nivel': self.procesa_nivel,
                       },})
            #for row in rows:
            for line in report.account_ids.filtered(lambda x:not x.hide_line):
                subctade = ''
                internal_level = ''
                cuenta_sat = ''
                cuenta_tipo = ''
                if line.account_id:
                    internal_level = line.account_id.group_id.level + 2 or '' #internal_level or ''
                    cuenta_sat = line.account_id.group_id.cuenta_sat or ''
                    cuenta_tipo = line.account_id.group_id.cuenta_tipo or ''
                    subctade = line.account_id.group_id.code_prefix or ''
                elif line.account_group_id:
                    if line.account_group_id.parent_id and line.account_group_id.parent_id.code_prefix:
                        subctade = line.account_group_id.parent_id.code_prefix
                    internal_level = line.level + 1 or '' #account_group_id.internal_level or ''
                    cuenta_sat = line.account_group_id.cuenta_sat or ''
                    cuenta_tipo = line.account_group_id.cuenta_tipo or ''
                    if not cuenta_sat or not cuenta_tipo:
                        account_exist = account_obj.search([('name','=',line.account_group_id.name),('code','=',line.account_group_id.code_prefix)], limit=1)
                        if account_exist:
                            if not cuenta_sat:
                                cuenta_sat = account_exist.cuenta_sat or ''
                            if not cuenta_tipo:
                                cuenta_tipo = account_exist.cuenta_tipo or ''
                        
                account_lines.append({'subctade': subctade,
                                      'codagrup': cuenta_sat,
                                      'numcta': line.code,
                                      'desc': line.name,
                                      'nivel': internal_level,
                                      'natur': cuenta_tipo})
        else:
            request_params.update({'informacion':{
                      'proceso': 'balanza',
                      'fecha_mes': self.fecha_mes,
                      'fecha_ano': self.fecha_ano,
                      'procesa_nivel': self.procesa_nivel,
                       },})
            for line in report.account_ids.filtered(lambda x:not x.hide_line):
                
                account_lines.append({'numcta': line.code,
                                      'saldoini': line.initial_balance,
                                      'debe': line.debit,
                                      'haber': line.credit,
                                      'saldofin': line.final_balance,
                                      })
        request_params.update({'accounts': account_lines})
        return request_params
    

    @api.multi
    def action_validate_xml(self):
        ctx = self._context.copy()
        report = self.env['report_trial_balance'].browse(ctx.get('active_id'))
        values = self.to_json(report)
        
        url=''
        company = self.env.user.company_id
        if company.proveedor_timbrado == 'multifactura':
            url = '%s' % ('http://ec2-54-245-3-122.us-west-2.compute.amazonaws.com/api/contabilidad')
        elif company.proveedor_timbrado == 'gecoerp':
            if company.modo_prueba:
                url = '%s' % ('https://itadmin.gecoerp.com/invoice/?handler=OdooHandler33')
            else:
                url = '%s' % ('https://itadmin.gecoerp.com/invoice/?handler=OdooHandler33')
        response = requests.post(url,auth=None,verify=False, data=json.dumps(values),headers={"Content-type": "application/json"})
        #_logger.info('something ... %s', response.text)

        json_response = response.json()
        estado_factura = json_response.get('estado_conta','')
        if estado_factura == 'problemas_contabilidad':
            raise UserError(_(json_response['problemas_message']))
        if json_response.get('conta_xml'):
            
            #_logger.info("xml %s", json_response['conta_xml'])
            #_logger.info("zip %s", json_response['conta_zip'])

            #return base64.b64decode(json_response['conta_xml'])
            try:
                form_id = self.env['ir.model.data'].get_object_reference('contabilidad_cfdi', 'reporte_conta_xml_zip_download_wizard_download_form_view_itadmin')[1]
            except ValueError:
                form_id = False
            ctx.update({'default_xml_data': json_response['conta_xml'], 'default_zip_data': json_response.get('conta_zip', None)})    
            return {
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'conta.xml.zip.download',
                'views': [(form_id, 'form')],
                'view_id': form_id,
                'target': 'new',
                'context': ctx,
            }
        return True
    
class ContaXMLZIPDownload(models.TransientModel):
    _name = 'conta.xml.zip.download'
    
    xml_data = fields.Binary("XML File")
    zip_data = fields.Binary("Zip File")
    
    @api.multi
    def download_xml_zip_file(self):
        if self._context.get('file_type','')=='zip':
            field_name = 'zip_data'
            filename = '%s.zip'%(datetime.today().strftime("%Y_%m_%d_%H_%M_%S"))
        else:
            field_name = 'xml_data'
            filename = '%s.xml'%(datetime.today().strftime("%Y_%m_%d_%H_%M_%S"))
        
        try:
            form_id = self.env['ir.model.data'].get_object_reference('contabilidad_cfdi', 'reporte_conta_xml_zip_download_wizard_download_form_view_itadmin')[1]
        except ValueError:
            form_id = False
        #ctx.update({'default_xml_data': json_response['conta_xml'], 'default_zip_data': json_response.get('conta_zip', None)})    
        ctx = self._context.copy()
        return {
              'type': 'ir.actions.act_multi_print',
              'actions': [
                          {
                            'type' : 'ir.actions.act_url',
                            'url': "/web/content/?model="+self._name+"&id=" + str(self.id) + "&field="+field_name+"&download=true&filename="+filename,
                            'target':'self',
                            'context': ctx,
                          },
                          {
                            'type': 'ir.actions.act_window',
                            'view_type': 'form',
                            'view_mode': 'form',
                            'res_model': 'conta.xml.zip.download',
                            'views': [(form_id, 'form')],
                            'view_id': form_id,
                            'target': 'new',
                            'res_id': self.id,
                            'context': ctx,
                        }
              ]
           }
                
#         return {
#                 'type' : 'ir.actions.act_url',
#                 'url': "/web/content/?model="+self._name+"&id=" + str(self.id) + "&field="+field_name+"&download=true&filename="+filename,
#                 'target':'self',
#                 }
#         
#         return True