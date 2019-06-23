# -*- coding: utf-8 -*-
import base64
import json
import requests
from odoo import fields, models,api, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta

class ResCompany(models.Model):
    _inherit = 'res.company'

    rfc = fields.Char(string=_('RFC'))
    proveedor_timbrado= fields.Selection(
        selection=[('gecoerp', _('GecoERP')),
                   ('multifactura', _('Multifacturas')),],
        string=_('Proveedor de timbrado'), 
    )
    api_key = fields.Char(string=_('API Key'))
    http_factura = fields.Char(string=_('HTTP Factura'))
    factura_dir = fields.Char(string=_('Directorio XML'))
    modo_prueba = fields.Boolean(string=_('Modo prueba'))
    regimen_fiscal = fields.Selection(
        selection=[('601', _('General de Ley Personas Morales')),
                   ('603', _('Personas Morales con Fines no Lucrativos')),
                   ('605', _('Sueldos y Salarios e Ingresos Asimilados a Salarios')),
                   ('606', _('Arrendamiento')),
                   ('608', _('Demás ingresos')),
                   ('609', _('Consolidación')),
                   ('610', _('Residentes en el Extranjero sin Establecimiento Permanente en México')),
                   ('611', _('Ingresos por Dividendos (socios y accionistas)')),
                   ('612', _('Personas Físicas con Actividades Empresariales y Profesionales')),
                   ('614', _('Ingresos por intereses')),
                   ('616', _('Sin obligaciones fiscales')),
                   ('620', _('Sociedades Cooperativas de Producción que optan por diferir sus ingresos')),
                   ('621', _('Incorporación Fiscal')),
                   ('622', _('Actividades Agrícolas, Ganaderas, Silvícolas y Pesqueras')),
                   ('623', _('Opcional para Grupos de Sociedades')),
                   ('624', _('Coordinados')),
                   ('628', _('Hidrocarburos')),
                   ('607', _('Régimen de Enajenación o Adquisición de Bienes')),
                   ('629', _('De los Regímenes Fiscales Preferentes y de las Empresas Multinacionales')),
                   ('630', _('Enajenación de acciones en bolsa de valores')),
                   ('615', _('Régimen de los ingresos por obtención de premios')),],
        string=_('Régimen Fiscal'), 
    )
    archivo_cer = fields.Binary(string=_('Archivo .cer'))
    archivo_key = fields.Binary(string=_('Archivo .key'))
    contrasena = fields.Char(string=_('Contraseña'))
    nombre_fiscal = fields.Char(string=_('Razón social'))
    saldo_timbres =  fields.Float(string=_('Saldo de timbres'), readonly=True)
    saldo_alarma =  fields.Float(string=_('Alarma timbres'), default=0)
    correo_alarma =  fields.Char(string=_('Correo de alarma'))
    telefono_sms = fields.Char(string=_('Teléfono celular'))  

    rfc_patron = fields.Char(string=_('RFC Patrón'))
    serie_nomina = fields.Char(string=_('Serie nomina'))
    registro_patronal = fields.Char(string=_('Registro patronal'))
    #nomina_mail = fields.Many2one("mail.template", 'Nomina Mail',)
    nomina_mail = fields.Char('Nomina Mail',)
    
    @api.model
    def contract_warning_mail_cron(self):
        companies = self.search([('nomina_mail','!=',False)])
        cr = self._cr
        dt = datetime.now()
        start_week_day = (dt - timedelta(days=dt.weekday())).date()
        end_week_day = start_week_day + timedelta(days=6)
        
        where_clause = []
        while start_week_day<=end_week_day:
            where_clause.append("TO_CHAR(date_start,'MM-DD')='%s-%s'"%("{0:0=2d}".format(start_week_day.month),"{0:0=2d}".format(start_week_day.day)))
            start_week_day = start_week_day + timedelta(days=1) #.date()
        where_clause = " OR ".join(where_clause)
        
        for company in companies:
            cr.execute("select id from hr_contract where (%s) and company_id=%d"%(where_clause,company.id))
            contract_ids = [r[0] for r in cr.fetchall()]
            if not contract_ids:
                continue
            for contract in self.env['hr.contract'].browse(contract_ids):
                #self.env['hr.contract'].browse(contract_ids)
                if not contract.employee_id.work_email:
                    continue
                
                mail_values = {
                    #'email_from': contract.employee_id.work_email,
                    #'reply_to': mailing.reply_to,
                    'email_to': company.nomina_mail,
                    'subject': '',
                    'body_html': 'Esta semana cumpleaños ' +  contract.employee_id.name + ' en la empresa, revisar ajuste en sueldo diario integrado.',
                    'notification': True,
                    #'mailing_id': mailing.id,
                    #'attachment_ids': [(4, attachment.id) for attachment in mailing.attachment_ids],
                    'auto_delete': True,
                }
                mail = self.env['mail.mail'].create(mail_values)
                mail.send()
                self.calculate_contract_vacaciones(contract)
                #self.calculate_sueldo_diario_integrado(contract)
                #company.nomina_mail.send_mail(contract_id, force_send=True )
        return
    
    @api.model
    def calculate_contract_vacaciones(self, contract):
        tablas_cfdi = contract.tablas_cfdi_id
        if not tablas_cfdi:
            tablas_cfdi = self.env['tablas.cfdi'].search([],limit=1)
        if not tablas_cfdi:
            return
        antiguedad_anos = contract.antiguedad_anos
        if antiguedad_anos < 1.0:
            tablas_cfdi_lines = tablas_cfdi.tabla_antiguedades.filtered(lambda x: x.antiguedad >= antiguedad_anos).sorted(key=lambda x:x.antiguedad)
        else:
            tablas_cfdi_lines = tablas_cfdi.tabla_antiguedades.filtered(lambda x: x.antiguedad <= antiguedad_anos).sorted(key=lambda x:x.antiguedad, reverse=True)
        if not tablas_cfdi_lines:
            return
        tablas_cfdi_line = tablas_cfdi_lines[0]
        today = datetime.today()
        current_year = today.strftime('%Y')
        contract.write({'tabla_vacaciones': [(0, 0, {'ano':current_year, 'dias': tablas_cfdi_line.vacaciones})]})
        return True
    
    @api.model
    def calculate_sueldo_diario_integrado(self, contract):
        if contract.date_start:
            today = datetime.today().date()
            diff_date = (today - contract.date_start + timedelta(days=1)).days #today - date_start 
            years = diff_date /365.0
            tablas_cfdi = contract.tablas_cfdi_id
            if not tablas_cfdi:
                tablas_cfdi = self.env['tablas.cfdi'].search([],limit=1)
            if not tablas_cfdi:
                return
            if years < 1.0:
                tablas_cfdi_lines = tablas_cfdi.tabla_antiguedades.filtered(lambda x: x.antiguedad >= years).sorted(key=lambda x:x.antiguedad)
            else:
                tablas_cfdi_lines = tablas_cfdi.tabla_antiguedades.filtered(lambda x: x.antiguedad <= years).sorted(key=lambda x:x.antiguedad, reverse=True)
            if not tablas_cfdi_lines:
                return
            tablas_cfdi_line = tablas_cfdi_lines[0]
            sueldo_diario_integrado = ((365 + tablas_cfdi_line.aguinaldo + (tablas_cfdi_line.vacaciones)* (tablas_cfdi_line.prima_vac/100) ) / 365) * contract.wage/30
            if sueldo_diario_integrado > (tablas_cfdi.uma * 25):
                sueldo_diario_integrado = tablas_cfdi.uma * 25
            contract.write({'sueldo_diario_integrado': sueldo_diario_integrado})
        return
    
    @api.model
    def get_saldo_by_cron(self):
        companies = self.search([('proveedor_timbrado','!=',False)])
        for company in companies:
            company.get_saldo()
            if company.saldo_timbres < company.saldo_alarma and company.correo_alarma:
                email_template = self.env.ref("nomina_cfdi_ee.email_template_alarma_de_saldo",False)
                if not email_template:return
                emails = company.correo_alarma.split(",")
                for email in emails:
                    email = email.strip()
                    if email:
                        email_template.send_mail(company.id, force_send=True,email_values={'email_to':email})
        return True    
    
    def get_saldo(self):
        values = {
                 'rfc': self.rfc,
                 'api_key': self.proveedor_timbrado,
                 'modo_prueba': self.modo_prueba,
                 }
        url=''
        if self.proveedor_timbrado == 'multifactura':
            url = '%s' % ('http://facturacion.itadmin.com.mx/api/saldo')
        elif self.proveedor_timbrado == 'gecoerp':
            if self.modo_prueba:
                #url = '%s' % ('https://ws.gecoerp.com/itadmin/pruebas/invoice/?handler=OdooHandler33')
                url = '%s' % ('https://itadmin.gecoerp.com/invoice/?handler=OdooHandler33')
            else:
                url = '%s' % ('https://itadmin.gecoerp.com/invoice/?handler=OdooHandler33')
        if not url:
            return
        try:
            response = requests.post(url,auth=None,verify=False, data=json.dumps(values),headers={"Content-type": "application/json"})
            json_response = response.json()
        except Exception as e:
            print(e)
            json_response = {}
    
        if not json_response:
            return
        
        estado_factura = json_response['estado_saldo']
        if estado_factura == 'problemas_saldo':
            raise UserError(_(json_response['problemas_message']))
        if json_response.get('saldo'):
            xml_saldo = base64.b64decode(json_response['saldo'])
        values2 = {
                    'saldo_timbres': xml_saldo
                  }
        self.update(values2)

    @api.multi
    def button_dummy(self):
        self.get_saldo()
        return True