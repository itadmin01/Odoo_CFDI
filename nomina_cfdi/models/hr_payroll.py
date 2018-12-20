# -*- coding: utf-8 -*-

import base64
import json
import requests
from lxml import etree
import datetime
from datetime import timedelta
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from reportlab.graphics.barcode import createBarcodeDrawing, getCodes
from reportlab.lib.units import mm
import logging
_logger = logging.getLogger(__name__)
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF, DEFAULT_SERVER_DATETIME_FORMAT as DTF 

class HrSalaryRule(models.Model):
    #_inherit = ['hr.salary.rule','mail.thread']
    _inherit = 'hr.salary.rule'
    tipo_percepcion = fields.Selection(
        selection=[('001', 'Sueldos, Salarios  Rayas y Jornales'), 
                   ('002', 'Gratificación Anual (Aguinaldo)'), 
                   ('003', 'Participación de los Trabajadores en las Utilidades PTU'),
                   ('004', 'Reembolso de Gastos Médicos Dentales y Hospitalarios'), 
                   ('005', 'Fondo de ahorro'),
                   ('006', 'Caja de ahorro'),
                   ('009', 'Contribuciones a Cargo del Trabajador Pagadas por el Patrón'), 
                   ('010', 'Premios por puntualidad'),
                   ('011', 'Prima de Seguro de vida'), 
                   ('012', 'Seguro de Gastos Médicos Mayores'), 
                   ('013', 'Cuotas Sindicales Pagadas por el Patrón'), 
                   ('014', 'Subsidios por incapacidad'),
                   ('015', 'Becas para trabajadores y/o hijos'), 
                   ('019', 'Horas extra'),
                   ('020', 'Prima dominical'), 
                   ('021', 'Prima vacacional'),
                   ('022', 'Prima por antigüedad'),
                   ('023', 'Pagos por separación'),
                   ('024', 'Seguro de retiro'),
                   ('025', 'Indemnizaciones'), 
                   ('026', 'Reembolso por funeral'), 
                   ('027', 'Cuotas de seguridad social pagadas por el patrón'), 
                   ('028', 'Comisiones'),
                   ('029', 'Vales de despensa'),
                   ('030', 'Vales de restaurante'), 
                   ('031', 'Vales de gasolina'),
                   ('032', 'Vales de ropa'), 
                   ('033', 'Ayuda para renta'), 
                   ('034', 'Ayuda para artículos escolares'), 
                   ('035', 'Ayuda para anteojos'),
                   ('036', 'Ayuda para transporte'), 
                   ('037', 'Ayuda para gastos de funeral'),
                   ('038', 'Otros ingresos por salarios'), 
                   ('039', 'Jubilaciones, pensiones o haberes de retiro'),
                   ('044', 'Jubilaciones, pensiones o haberes de retiro en parcialidades'),
                   ('045', 'Ingresos en acciones o títulos valor que representan bienes'),
                   ('046', 'Ingresos asimilados a salarios'),
                   ('047', 'Alimentación'), 
                   ('048', 'Habitación'), 
                   ('049', 'Premios por asistencia'), 
                   ('050', 'Viáticos'),],
        string=_('Tipo de percepción'),
    )
    tipo_deduccion = fields.Selection(
        selection=[('001', 'Seguridad social'), 
                   ('002', 'ISR'), 
                   ('003', 'Aportaciones a retiro, cesantía en edad avanzada y vejez.'),
                   ('004', 'Otros'), 
                   ('005', 'Aportaciones a Fondo de vivienda'),
                   ('006', 'Descuento por incapacidad'),
                   ('007', 'Pensión alimenticia'),
                   ('008', 'Renta'),				   
                   ('009', 'Préstamos provenientes del Fondo Nacional de la Vivienda para los Trabajadores'), 
                   ('010', 'Pago por crédito de vivienda'),
                   ('011', 'Pago de abonos INFONACOT'), 
                   ('012', 'Anticipo de salarios'), 
                   ('013', 'Pagos hechos con exceso al trabajador'), 
                   ('014', 'Errores'),
                   ('015', 'Pérdidas'), 
                   ('016', 'Averías'), 
                   ('017', 'Adquisición de artículos producidos por la empresa o establecimiento'),
                   ('018', 'Cuotas para la constitución y fomento de sociedades cooperativas y de cajas de ahorro'), 				   
                   ('019', 'Cuotas sindicales'),
                   ('020', 'Ausencia (Ausentismo)'), 
                   ('021', 'Cuotas obrero patronales'),
                   ('022', 'Impuestos Locales'),
                   ('023', 'Aportaciones voluntarias'),
                   ('101', 'ISR Retenido de ejercicio anterior'),],
        string=_('Tipo de deducción'),
    )

    tipo_otro_pago = fields.Selection(
        selection=[('001', 'Reintegro de ISR pagado en exceso'), 
                   ('002', 'Subsidio para el empleo'), 
                   ('003', 'Viáticos'),
                   ('004', 'Aplicación de saldo a favor por compensación anual'), 
                   ('005', 'Reintegro de ISR retenido en exceso de ejercicio anterior'),
                   ('999', 'Pagos distintos a los listados y que no deben considerarse como ingreso por sueldos, salarios o ingresos asimilados'),],
        string=_('Otros Pagos'),)
    category_code = fields.Char("Category Code",related="category_id.code",store=True)
    
class HrPayslip(models.Model):
    _name = "hr.payslip"
    _inherit = ['hr.payslip','mail.thread']

    tipo_nomina = fields.Selection(
        selection=[('O', 'Nómina ordinaria'), 
                   ('E', 'Nómina extraordinaria'),],
        string=_('Tipo de nómina'), required=True, default='O'
    )

    estado_factura = fields.Selection(
        selection=[('factura_no_generada', 'Factura no generada'), ('factura_correcta', 'Factura correcta'), 
                   ('problemas_factura', 'Problemas con la factura'), ('factura_cancelada', 'Factura cancelada'), ],
        string=_('Estado de factura'),
        default='factura_no_generada',
        readonly=True
    )	
    imss_dias = fields.Float('Días a cotizar en la nómina',default='15') 
    imss_mes = fields.Float('Dias Periodo Mensual para IMSS',default='30.4')
    xml_nomina_link = fields.Char(string=_('XML link'), readonly=True)
    nomina_cfdi = fields.Boolean('Nomina CFDI')
    qrcode_image = fields.Binary("QRCode")
    qr_value = fields.Char(string=_('QR Code Value'))
    numero_cetificado = fields.Char(string=_('Numero de cetificado'))
    cetificaso_sat = fields.Char(string=_('Cetificao SAT'))
    folio_fiscal = fields.Char(string=_('Folio Fiscal'), readonly=True)
    fecha_certificacion = fields.Char(string=_('Fecha y Hora Certificación'))
    cadena_origenal = fields.Char(string=_('Cadena Origenal del Complemento digital de SAT'))
    selo_digital_cdfi = fields.Char(string=_('Selo Digital del CDFI'))
    selo_sat = fields.Char(string=_('Selo del SAT'))
    moneda = fields.Char(string=_('Moneda'))
    tipocambio = fields.Char(string=_('TipoCambio'))
    folio = fields.Char(string=_('Folio'))
    version = fields.Char(string=_('Version'))
    serie_emisor = fields.Char(string=_('Serie'))
    invoice_datetime = fields.Char(string=_('fecha factura'))
    rfc_emisor = fields.Char(string=_('RFC'))
    total_nomina = fields.Float('Total a pagar')
    subtotal = fields.Float('Subtotal')
    descuento = fields.Float('Descuento')
    deducciones_lines = []
    number_folio = fields.Char(string=_('Folio'), compute='_get_number_folio')
    fecha_factura = fields.Datetime(string=_('Fecha Factura'), readonly=True)
    subsidio_periodo = fields.Float('subsidio_periodo')
    isr_periodo = fields.Float('isr_periodo')
    retencion_subsidio_pagado = fields.Float('retencion_subsidio_pagado')
    importe_imss = fields.Float('importe_imss')
    importe_isr = fields.Float('importe_isr')
    periodicidad = fields.Float('periodicidad')

    forma_pago = fields.Selection(
        selection=[('99', '99 - Por definir'),],
        string=_('Forma de pago'),default='99',
    )	
    tipo_comprobante = fields.Selection(
        selection=[('N', 'Nómina'),],
        string=_('Tipo de comprobante'),default='N',
    )	
    tipo_relacion = fields.Selection(
        selection=[('04', 'Sustitución de los CFDI previos'),],
        string=_('Tipo relación'),
    )
    uuid_relacionado = fields.Char(string=_('CFDI Relacionado'))
    methodo_pago = fields.Selection(
        selection=[('PUE', _('Pago en una sola exhibición')),],
        string=_('Método de pago'), default='PUE',
    )	
    uso_cfdi = fields.Selection(
        selection=[('P01', _('Por definir')),],
        string=_('Uso CFDI (cliente)'),default='P01',
    )
    fecha_pago = fields.Date(string=_('Fecha de pago'))

    @api.multi
    @api.onchange('date_to')
    def _get_fecha_pago(self):
        if self.date_to:
            values = {
                'fecha_pago': self.date_to
                }
            self.update(values)
    
    @api.model
    def create(self, vals):
        if not vals.get('fecha_pago') and vals.get('date_to'):
            vals.update({'fecha_pago': vals.get('date_to')})
            
        res = super(HrPayslip, self).create(vals)
        return res
    
    @api.depends('number')
    @api.one
    def _get_number_folio(self):
        if self.number:
            self.number_folio = self.number.replace('SLIP','').replace('/','')

    @api.one
    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        default = dict(default or {})
        if self.estado_factura == 'factura_correcta':
            default['estado_factura'] = 'factura_no_generada'
            default['folio_fiscal'] = ''
            default['fecha_factura'] = None         
            default['nomina_cfdi'] = False
        return super(HrPayslip, self).copy(default=default)

    @api.model
    def to_json(self):
        payslip_total_TOP = 0
        payslip_total_TDED = 0
        payslip_total_PERG = 0
        payslip_total_PERE = 0	
        antiguedad = 1
        if self.contract_id.date_end and self.contract_id.date_start:
            #antiguedad = int((datetime.datetime.strptime(self.contract_id.date_end, "%Y-%m-%d") - datetime.datetime.strptime(self.contract_id.date_start, "%Y-%m-%d") + timedelta(days=1)).days/7)
            antiguedad = int((self.contract_id.date_end - self.contract_id.date_start + timedelta(days=1)).days/7)
        elif self.date_to and self.contract_id.date_start:
            #antiguedad = int((datetime.datetime.strptime(self.date_to, "%Y-%m-%d") - datetime.datetime.strptime(self.contract_id.date_start, "%Y-%m-%d") + timedelta(days=1)).days/7)
            antiguedad = int((self.date_to - self.contract_id.date_start + timedelta(days=1)).days/7)

#**********  Percepciones ************
        total_percepciones_lines = self.env['hr.payslip.line'].search(['|',('category_id.name','=','Percepciones gravadas'),('code','=','101'),('category_id.name','=','Otros Pagos'),('slip_id','=',self.id)])
        percepciones_grabadas_lines = self.env['hr.payslip.line'].search(['|',('category_id.name','=','Percepciones gravadas'),('code','=','101'),('slip_id','=',self.id)])
        lineas_de_percepcion = []
        tipo_percepcion_dict = dict(self.env['hr.salary.rule']._fields.get('tipo_percepcion').selection)
        if percepciones_grabadas_lines:
            for line in percepciones_grabadas_lines:
                payslip_total_PERG += round(line.total,2)
                lineas_de_percepcion.append({'TipoPercepcion': line.salary_rule_id.tipo_percepcion,
                'Clave': line.code,
                'Concepto': tipo_percepcion_dict.get(line.salary_rule_id.tipo_percepcion),
                'ImporteGravado': line.total,
                'ImporteExento': '0'})

        percepciones_excentas_lines = self.env['hr.payslip.line'].search([('category_id.name','=','Percepciones excentas'),('slip_id','=',self.id)])
        lineas_de_percepcion_exentas = []
        if percepciones_excentas_lines:
            for line in percepciones_excentas_lines:
                payslip_total_PERE += round(line.total,2)
                lineas_de_percepcion_exentas.append({'TipoPercepcion': line.salary_rule_id.tipo_percepcion,
                'Clave': line.code,
                'Concepto': tipo_percepcion_dict.get(line.salary_rule_id.tipo_percepcion),
                'ImporteGravado': '0',
                'ImporteExento': line.total})

        percepcion = {
               'Totalpercepcion': {
                        'TotalGravado': payslip_total_PERG,
                        'TotalExento': payslip_total_PERE,
                        'TotalSueldos': payslip_total_PERG + payslip_total_PERE,
               },
        }

        percepcion.update({'lineas_de_percepcion_grabadas': lineas_de_percepcion, 'no_per_grabadas': len(percepciones_grabadas_lines)})
        percepcion.update({'lineas_de_percepcion_excentas': lineas_de_percepcion_exentas, 'no_per_excentas': len(percepciones_excentas_lines)})
        request_params = {'percepciones': percepcion}

#****** OTROS PAGOS ******
        otrospagos_lines = self.env['hr.payslip.line'].search([('category_id.name','=','Otros Pagos'),('slip_id','=',self.id)])
        tipo_otro_pago_dict = dict(self.env['hr.salary.rule']._fields.get('tipo_otro_pago').selection)
        lineas_de_otros = []
        if otrospagos_lines:
            for line in otrospagos_lines:
                #logger.info('line total ...%s', line.total)
                if line.code == '201' and line.total > 0:
                    line2 = self.contract_id.env['tablas.subsidio.line'].search([('form_id','=',self.contract_id.tablas_cfdi_id.id),('lim_inf','<=',self.contract_id.wage)],order='lim_inf desc',limit=1)
                    self.subsidio_periodo = 0
                    #_logger.info('entro a este ..')
                    payslip_total_TOP += line.total
                    if line2:
                        self.subsidio_periodo = (line2.s_mensual/self.imss_mes)*self.imss_dias
                    lineas_de_otros.append({'TipoOtrosPagos': line.salary_rule_id.tipo_otro_pago,
                    'Clave': line.code,
                    'Concepto': tipo_otro_pago_dict.get(line.salary_rule_id.tipo_otro_pago),
                    'ImporteGravado': '0',
                    'ImporteExento': line.total,
                    'SubsidioCausado': self.subsidio_periodo})
                else:
                    payslip_total_TOP += line.total
                    #_logger.info('entro al otro ..')
                    lineas_de_otros.append({'TipoOtrosPagos': line.salary_rule_id.tipo_otro_pago,
                        'Clave': line.code,
                        'Concepto': tipo_otro_pago_dict.get(line.salary_rule_id.tipo_otro_pago),
                        'ImporteGravado': '0',
                        'ImporteExento': line.total})
        otrospagos = {
            'otrospagos': {
                    'Totalotrospagos': payslip_total_TOP,
            },
        }
        otrospagos.update({'otros_pagos': lineas_de_otros, 'no_otros_pagos': len(otrospagos_lines)})
        request_params.update({'otros_pagos': otrospagos})

#********** DEDUCCIONES *********
        total_imp_ret = 0
        suma_deducciones = 0
        self.importe_isr = 0
        self.isr_periodo = 0
        no_deuducciones = 0 #len(self.deducciones_lines)
        self.deducciones_lines = self.env['hr.payslip.line'].search([('category_id.name','=','Deducciones'),('slip_id','=',self.id)])
        #ded_impuestos_lines = self.env['hr.payslip.line'].search([('category_id.name','=','Deducciones'),('code','=','301'),('slip_id','=',self.id)],limit=1)
        tipo_deduccion_dict = dict(self.env['hr.salary.rule']._fields.get('tipo_deduccion').selection)
        #if ded_impuestos_lines:
        #   total_imp_ret = round(ded_impuestos_lines.total,2)
        lineas_deduccion = []
        if self.deducciones_lines:
            _logger.info('entro duduciones ...')
            #todas las deducciones excepto imss e isr
            for line in self.deducciones_lines:
                if line.salary_rule_id.tipo_deduccion != '001' and line.salary_rule_id.tipo_deduccion != '002':
                    #_logger.info('linea  ...')
                    no_deuducciones += 1
                    lineas_deduccion.append({'TipoDeduccion': line.salary_rule_id.tipo_deduccion,
                   'Clave': line.code,
                   'Concepto': tipo_deduccion_dict.get(line.salary_rule_id.tipo_deduccion),
                   'Importe': round(line.total,2)})
                    payslip_total_TDED += round(line.total,2)

            #todas las deducciones imss
            self.importe_imss = 0
            for line in self.deducciones_lines:
                if line.salary_rule_id.tipo_deduccion == '001':
                    #_logger.info('linea imss ...')
                    self.importe_imss += round(line.total,2)

            if self.importe_imss > 0:
                no_deuducciones += 1
                lineas_deduccion.append({'TipoDeduccion': '001',
                  'Clave': '302',
                  'Concepto': 'Seguridad social',
                  'Importe': round(self.importe_imss,2)})
                payslip_total_TDED += round(self.importe_imss,2)

            #todas las deducciones isr
            for line in self.deducciones_lines:
                if line.salary_rule_id.tipo_deduccion == '002' and line.salary_rule_id.code == 'ISR':
                    self.isr_periodo = line.total 
                if line.salary_rule_id.tipo_deduccion == '002':
                    #_logger.info('linea ISR ...')
                    self.importe_isr += round(line.total,2)

            if self.importe_isr > 0:
                no_deuducciones += 1
                lineas_deduccion.append({'TipoDeduccion': '002',
                  'Clave': '301',
                  'Concepto': 'ISR',
                  'Importe': round(self.importe_isr,2)})
                payslip_total_TDED += round(self.importe_isr,2)
            total_imp_ret = round(self.importe_isr,2)

        deduccion = {
            'TotalDeduccion': {
                    'TotalOtrasDeducciones': round(payslip_total_TDED - total_imp_ret,2),
                    'TotalImpuestosRetenidos': total_imp_ret,
            },
        }
        deduccion.update({'lineas_de_deduccion': lineas_deduccion, 'no_deuducciones': no_deuducciones})
        request_params.update({'deducciones': deduccion})

        self.retencion_subsidio_pagado = self.isr_periodo - self.subsidio_periodo
        self.total_nomina = payslip_total_PERG + payslip_total_PERE + payslip_total_TOP - payslip_total_TDED
        self.subtotal =  payslip_total_PERG + payslip_total_PERE + payslip_total_TOP
        self.descuento = payslip_total_TDED
        
        NumDiasPagados = 1
        if self.date_to and self.date_from:
            NumDiasPagados = (self.date_to - self.date_from + timedelta(days=1)).days
        request_params.update({
                'factura': {
                      'serie': self.company_id.serie_nomina,
                      'folio': self.number_folio,
                      'metodo_pago': self.methodo_pago,
                      'forma_pago': self.forma_pago,
                      'tipocomprobante': self.tipo_comprobante,
                      'moneda': 'MXN',
                      'tipodecambio': '1.0000',
                      'fecha_factura': self.fecha_factura and self.fecha_factura.strftime(DTF),
                      'LugarExpedicion': self.company_id.zip,
                      'RegimenFiscal': self.company_id.regimen_fiscal,
                      'subtotal': self.subtotal,
                      'descuento': self.descuento,
                      'total': self.total_nomina,
                },
                'emisor': {
                      'rfc': self.company_id.rfc,
                      'api_key': self.company_id.proveedor_timbrado,
                      'modo_prueba': self.company_id.modo_prueba,
                      'nombre_fiscal': self.company_id.nombre_fiscal,
                      'telefono_sms': self.company_id.telefono_sms,
                },
                'receptor': {
                      'rfc': self.employee_id.rfc,
                      'nombre': self.employee_id.name,
                      'uso_cfdi': self.uso_cfdi,
                },
                'conceptos': {
                      'cantidad': '1.0',
                      'ClaveUnidad': 'ACT',
                      'ClaveProdServ': '84111505',
                      'descripcion': 'Pago de nómina',
                      'valorunitario': self.subtotal,
                      'importe':  self.subtotal,
                      'descuento': self.descuento,
                },
                'nomina12': {
                      'TipoNomina': self.tipo_nomina,
                      'FechaPago': self.fecha_pago and self.fecha_pago.strftime(DF),
                      'FechaInicialPago': self.date_from and self.date_from.strftime(DF),
                      'FechaFinalPago': self.date_to and self.date_to.strftime(DF),
                      #'NumDiasPagados': (datetime.datetime.strptime(self.date_to, "%Y-%m-%d") - datetime.datetime.strptime(self.date_from, "%Y-%m-%d") + timedelta(days=1)).days,
                      'NumDiasPagados': NumDiasPagados,
                      'TotalPercepciones': payslip_total_PERG + payslip_total_PERE,
                      'TotalDeducciones': self.descuento,
                      'TotalOtrosPagos': payslip_total_TOP,
                },
                'nomina12Emisor': {
                      'RegistroPatronal': self.company_id.registro_patronal,
                      'RfcPatronOrigen': self.company_id.rfc,
                },
                'nomina12Receptor': {
                      'ClaveEntFed': self.employee_id.estado.code,
                      'Curp': self.employee_id.curp,
                      'NumEmpleado': self.employee_id.no_empleado,
                      'PeriodicidadPago': self.periodicdad, #self.contract_id.periodicidad_pago,
                      'TipoContrato': self.employee_id.contrato,
                      'TipoRegimen': self.employee_id.regimen,
                      'Antiguedad': 'P' + str(antiguedad) + 'W',
                      'Banco': self.employee_id.banco.c_banco,
                      'CuentaBancaria': self.employee_id.no_cuenta,
                      'FechaInicioRelLaboral': self.contract_id.date_start and self.contract_id.date_start.strftime(DF),
                      'NumSeguridadSocial': self.employee_id.segurosocial,
                      'Puesto': self.employee_id.job_id.name,
                      'Departamento': self.employee_id.department_id.name,
                      'RiesgoPuesto': self.contract_id.riesgo_puesto,
                      'SalarioBaseCotApor': self.contract_id.sueldo_diario_integrado,
                      'SalarioDiarioIntegrado': self.contract_id.sueldo_diario_integrado,
                },
		})

#****** CERTIFICADOS *******
        if not self.company_id.archivo_cer:
            raise UserError(_('Archivo .cer path is missing.'))
        if not self.company_id.archivo_key:
            raise UserError(_('Archivo .key path is missing.'))
        archivo_cer = self.company_id.archivo_cer
        archivo_key = self.company_id.archivo_key
        request_params.update({
                'certificados': {
                      'archivo_cer': archivo_cer.decode("utf-8"),
                      'archivo_key': archivo_key.decode("utf-8"),
                      'contrasena': self.company_id.contrasena,
                }})
        return request_params

    @api.multi
    def action_cfdi_nomina_generate(self):
        for payslip in self:
            if payslip.fecha_factura == False:
                payslip.fecha_factura= datetime.datetime.now()
                payslip.write({'fecha_factura': payslip.fecha_factura})
            if payslip.estado_factura == 'factura_correcta':
                raise UserError(_('Error para timbrar factura, Factura ya generada.'))
            if payslip.estado_factura == 'factura_cancelada':
                raise UserError(_('Error para timbrar factura, Factura ya generada y cancelada.'))

            values = payslip.to_json()
            #  print json.dumps(values, indent=4, sort_keys=True)
            if payslip.company_id.proveedor_timbrado == 'multifactura':
                url = '%s' % ('http://facturacion.itadmin.com.mx/api/nomina')
            elif payslip.company_id.proveedor_timbrado == 'gecoerp':
                if self.company_id.modo_prueba:
                    url = '%s' % ('https://ws.gecoerp.com/itadmin/pruebas/nomina/?handler=OdooHandler33')
                else:
                    url = '%s' % ('https://itadmin.gecoerp.com/nomina/?handler=OdooHandler33')

            response = requests.post(url,auth=None,verify=False, data=json.dumps(values),headers={"Content-type": "application/json"})

            _logger.info('something ... %s', response.text)
            json_response = response.json()
            xml_file_link = False
            estado_factura = json_response['estado_factura']
            if estado_factura == 'problemas_factura':
                raise UserError(_(json_response['problemas_message']))
            # Receive and stroe XML 
            if json_response.get('factura_xml'):
                xml_file_link = payslip.company_id.factura_dir + '/' + payslip.name.replace('/', '_') + '.xml'
                xml_file = open(xml_file_link, 'w')
                xml_payment = base64.b64decode(json_response['factura_xml'])
                xml_file.write(xml_payment.decode("utf-8"))
                xml_file.close()
                payslip._set_data_from_xml(xml_payment)
                    
                xml_file_name = payslip.name.replace('/', '_') + '.xml'
                self.env['ir.attachment'].sudo().create(
                                            {
                                                'name': xml_file_name,
                                                'datas': json_response['factura_xml'],
                                                'datas_fname': xml_file_name,
                                                'res_model': self._name,
                                                'res_id': payslip.id,
                                                'type': 'binary'
                                            })	
                report = self.env['ir.actions.report']._get_report_from_name('nomina_cfdi.report_payslip')
                report_data = report.render_qweb_pdf([payslip.id])[0]
                pdf_file_name = payslip.name.replace('/', '_') + '.pdf'
                self.env['ir.attachment'].sudo().create(
                                            {
                                                'name': pdf_file_name,
                                                'datas': base64.b64encode(report_data),
                                                'datas_fname': pdf_file_name,
                                                'res_model': self._name,
                                                'res_id': payslip.id,
                                                'type': 'binary'
                                            })

            payslip.write({'estado_factura': estado_factura,
                    'xml_nomina_link': xml_file_link,
                    'nomina_cfdi': True})

    @api.one
    def _set_data_from_xml(self, xml_invoice):
        if not xml_invoice:
            return None
        NSMAP = {
                 'xsi':'http://www.w3.org/2001/XMLSchema-instance',
                 'cfdi':'http://www.sat.gob.mx/cfd/3', 
                 'tfd': 'http://www.sat.gob.mx/TimbreFiscalDigital',
                 }

        xml_data = etree.fromstring(xml_invoice)
        Emisor = xml_data.find('cfdi:Emisor', NSMAP)
        RegimenFiscal = Emisor.find('cfdi:RegimenFiscal', NSMAP)
        Complemento = xml_data.find('cfdi:Complemento', NSMAP)
        TimbreFiscalDigital = Complemento.find('tfd:TimbreFiscalDigital', NSMAP)
        
        self.rfc_emisor = Emisor.attrib['Rfc']
        self.name_emisor = Emisor.attrib['Nombre']
        self.tipocambio = xml_data.attrib['TipoCambio']
        #  self.tipo_comprobante = xml_data.attrib['TipoDeComprobante']
        self.moneda = xml_data.attrib['Moneda']
        self.numero_cetificado = xml_data.attrib['NoCertificado']
        self.cetificaso_sat = TimbreFiscalDigital.attrib['NoCertificadoSAT']
        self.fecha_certificacion = TimbreFiscalDigital.attrib['FechaTimbrado']
        self.selo_digital_cdfi = TimbreFiscalDigital.attrib['SelloCFD']
        self.selo_sat = TimbreFiscalDigital.attrib['SelloSAT']
        self.folio_fiscal = TimbreFiscalDigital.attrib['UUID']
        self.folio = xml_data.attrib['Folio']
        self.serie_emisor = xml_data.attrib['Serie']
        self.invoice_datetime = xml_data.attrib['Fecha']
        self.version = TimbreFiscalDigital.attrib['Version']
        self.cadena_origenal = '||%s|%s|%s|%s|%s||' % (self.version, self.folio_fiscal, self.fecha_certificacion, 
                                                         self.selo_digital_cdfi, self.cetificaso_sat)
        
        options = {'width': 275 * mm, 'height': 275 * mm}
        amount_str = str(self.total_nomina).split('.')
        #print 'amount_str, ', amount_str
        qr_value = '?re=%s&rr=%s&tt=%s.%s&id=%s' % (self.company_id.rfc, 
                                                 self.employee_id.rfc,
                                                 amount_str[0].zfill(10),
                                                 amount_str[1].ljust(6, '0'),
                                                 self.folio_fiscal
                                                 )
        self.qr_value = qr_value
        ret_val = createBarcodeDrawing('QR', value=qr_value, **options)
        self.qrcode_image = base64.encodestring(ret_val.asString('jpg'))

    @api.multi
    def action_cfdi_cancel(self):
        for payslip in self:
            if payslip.nomina_cfdi:
                if payslip.estado_factura == 'factura_cancelada':
                    pass
                    # raise UserError(_('La factura ya fue cancelada, no puede volver a cancelarse.'))
                if not payslip.company_id.archivo_cer:
                    raise UserError(_('Falta la ruta del archivo .cer'))
                if not payslip.company_id.archivo_key:
                    raise UserError(_('Falta la ruta del archivo .key'))
                archivo_cer = self.company_id.archivo_cer
                archivo_key = self.company_id.archivo_key
                values = {
                          'rfc': payslip.company_id.rfc,
                          'api_key': payslip.company_id.proveedor_timbrado,
                          'uuid': self.folio_fiscal,
                          'folio': self.folio,
                          'serie_factura': payslip.company_id.serie_nomina,
                          'modo_prueba': payslip.company_id.modo_prueba,
                            'certificados': {
                                  'archivo_cer': archivo_cer.decode("utf-8"),
                                  'archivo_key': archivo_key.decode("utf-8"),
                                  'contrasena': payslip.company_id.contrasena,
                            }
                          }
                if self.company_id.proveedor_timbrado == 'multifactura':
                    url = '%s' % ('http://facturacion.itadmin.com.mx/api/refund')
                elif self.company_id.proveedor_timbrado == 'gecoerp':
                    if self.company_id.modo_prueba:
                        url = '%s' % ('https://ws.gecoerp.com/itadmin/pruebas/refund/?handler=OdooHandler33')
                        #url = '%s' % ('https://itadmin.gecoerp.com/refund/?handler=OdooHandler33')
                    else:
                        url = '%s' % ('https://itadmin.gecoerp.com/refund/?handler=OdooHandler33')
                response = requests.post(url , 
                                         auth=None,verify=False, data=json.dumps(values), 
                                         headers={"Content-type": "application/json"})
    
                #print 'Response: ', response.status_code
                json_response = response.json()
                #_logger.info('log de la exception ... %s', response.text)

                if json_response['estado_factura'] == 'problemas_factura':
                    raise UserError(_(json_response['problemas_message']))
                elif json_response.get('factura_xml', False):
                    if payslip.number:
                        xml_file_link = payslip.company_id.factura_dir + '/CANCEL_' + payslip.number.replace('/', '_') + '.xml'
                    else:
                        xml_file_link = payslip.company_id.factura_dir + '/CANCEL_' + self.folio_fiscal + '.xml'						
                    xml_file = open(xml_file_link, 'w')
                    xml_invoice = base64.b64decode(json_response['factura_xml'])
                    xml_file.write(xml_invoice.decode("utf-8"))
                    xml_file.close()
                    if payslip.number:
                        file_name = payslip.number.replace('/', '_') + '.xml'
                    else:
                        file_name = self.folio_fiscal + '.xml'
                    self.env['ir.attachment'].sudo().create(
                                                {
                                                    'name': file_name,
                                                    'datas': json_response['factura_xml'],
                                                    'datas_fname': file_name,
                                                    'res_model': self._name,
                                                    'res_id': payslip.id,
                                                    'type': 'binary'
                                                })
                payslip.write({'estado_factura': json_response['estado_factura']})

    @api.multi
    def send_nomina(self):
        self.ensure_one()
        template = self.env.ref('nomina_cfdi.email_template_payroll', False)
        compose_form = self.env.ref('mail.email_compose_message_wizard_form', False)
            
        ctx = dict()
        ctx.update({
            'default_model': 'hr.payslip',
            'default_res_id': self.id,
            'default_use_template': bool(template),
            'default_template_id': template.id,
            'default_composition_mode': 'comment',
        })
        return {
            'name': _('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        }

    @api.model
    def fondo_ahorro(self):	
        deducciones_ahorro = self.env['hr.payslip.line'].search([('category_id.name','=','Deducciones'),('slip_id','=',self.id)])
        if deducciones_ahorro:
            _logger.info('fondo ahorro deudccion...')
            for line in deducciones_ahorro:
                if line.salary_rule_id.code == 'DFA':
                    self.employee_id.fondo_ahorro += line.total

        percepciones_ahorro = self.env['hr.payslip.line'].search([('category_id.name','=','Percepciones excentas'),('slip_id','=',self.id)])
        if percepciones_ahorro:
            _logger.info('fondo ahorro percepcion...')
            for line in percepciones_ahorro:
                if line.salary_rule_id.code == 'PFA':
                    self.employee_id.fondo_ahorro -= line.total

    @api.model
    def devolucion_fondo_ahorro(self):	
        deducciones_ahorro = self.env['hr.payslip.line'].search([('category_id.name','=','Deducciones'),('slip_id','=',self.id)])
        if deducciones_ahorro:
            _logger.info('Devolucion fondo ahorro deduccion...')
            for line in deducciones_ahorro:
                if line.salary_rule_id.code == 'DFA':
                    self.employee_id.fondo_ahorro -= line.total

        percepciones_ahorro = self.env['hr.payslip.line'].search([('category_id.name','=','Percepciones excentas'),('slip_id','=',self.id)])
        if percepciones_ahorro:
            _logger.info('Devolucion fondo ahorro percepcion...')
            for line in percepciones_ahorro:
                if line.salary_rule_id.code == 'PFA':
                    self.employee_id.fondo_ahorro += line.total

    @api.multi
    def action_payslip_done(self):
        res = super(HrPayslip, self).action_payslip_done()
        for rec in self:
            rec.fondo_ahorro()
        return res

    @api.multi
    def refund_sheet(self):
        res = super(HrPayslip, self).refund_sheet()
        for rec in self:
            rec.devolucion_fondo_ahorro()
        return res


class HrPayslipMail(models.Model):
    _name = "hr.payslip.mail"
    _inherit = ['mail.thread']
    _description = "Nomina Mail"
   
    payslip_id = fields.Many2one('hr.payslip', string='Nomina')
    name = fields.Char(related='payslip_id.name')
    xml_nomina_link = fields.Char(related='payslip_id.xml_nomina_link')
    employee_id = fields.Many2one(related='payslip_id.employee_id')
    company_id = fields.Many2one(related='payslip_id.company_id')
    
class MailTemplate(models.Model):
    "Templates for sending email"
    _inherit = 'mail.template'
    
    @api.model
    def _get_file(self, url):
        url = url.encode('utf8')
        filename, headers = urllib.urlretrieve(url)
        fn, file_extension = os.path.splitext(filename)
        return  filename, file_extension.replace('.', '')

    @api.multi
    def generate_email(self, res_ids, fields=None):
        results = super(MailTemplate, self).generate_email(res_ids, fields=fields)
        
        if isinstance(res_ids, (int)):
            res_ids = [res_ids]
        res_ids_to_templates = super(MailTemplate, self).get_email_template(res_ids)

        # templates: res_id -> template; template -> res_ids
        templates_to_res_ids = {}
        for res_id, template in res_ids_to_templates.items():
            templates_to_res_ids.setdefault(template, []).append(res_id)
        
        template_id = self.env.ref('nomina_cfdi.email_template_payroll')
        for template, template_res_ids in templates_to_res_ids.items():
            if template.id  == template_id.id:
                for res_id in template_res_ids:
                    payment = self.env[template.model].browse(res_id)
                    if payment.xml_nomina_link:
                        attachments =  results[res_id]['attachments'] or []
                        names = payment.xml_nomina_link.split('/')
                        fn = names[len(names) - 1]
                        data = open(payment.xml_nomina_link, 'rb').read()
                        attachments.append((fn, base64.b64encode(data)))
                        results[res_id]['attachments'] = attachments
        return results