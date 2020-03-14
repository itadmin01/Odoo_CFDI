# -*- coding: utf-8 -*-

import base64
import json
import requests
from lxml import etree
#import time
import datetime

from datetime import timedelta, date
#from datetime import time as datetime_time
#from dateutil import relativedelta
from pytz import timezone

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from reportlab.graphics.barcode import createBarcodeDrawing #, getCodes
from reportlab.lib.units import mm
import logging
_logger = logging.getLogger(__name__)
import pytz
#from .tzlocal import get_localzone
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF, DEFAULT_SERVER_DATETIME_FORMAT as DTF 

from collections import defaultdict

class HrSalaryRule(models.Model):
    _inherit = 'hr.salary.rule'

    tipo_cpercepcion = fields.Many2one('nomina.percepcion', string='Tipo de percepción')
    tipo_cdeduccion = fields.Many2one('nomina.deduccion', string='Tipo de deducción')
    tipo_cotro_pago = fields.Many2one('nomina.otropago', string='Otros Pagos')

    category_code = fields.Char("Category Code",related="category_id.code",store=True)

    forma_pago = fields.Selection(
        selection=[('001', 'Efectivo'), 
                   ('002', 'Especie'),],
        string=_('Forma de pago'),default='001')
    exencion = fields.Boolean('Percepción con exención de ISR')
    integrar_al_ingreso = fields.Selection(
        selection=[('001', 'Ordinaria'), 
                   ('002', 'Extraordinaria mensual'),
                   ('003', 'Extraordinaria anual'),
                   ('004', 'Parte exenta por día'),],
        string=_('Integrar al ingreso gravable como percepción'))
#    monto_exencion = fields.Float('Exención (UMA)', digits = (12,3))
    variable_imss = fields.Boolean('Percepción variable para el IMSS')
    variable_imss_tipo = fields.Selection(
        selection=[('001', 'Todo el monto'), 
                   ('002', 'Excedente del (% de UMA)'),
                   ('003', 'Excedente del (% de SBC)'),],
        string=_('Tipo'),default='001')
    variable_imss_monto = fields.Float('Monto')
    integrar_ptu = fields.Boolean('Integrar para el PTU')
    integrar_estatal = fields.Boolean('Integrar para el impuesto estatal')
    parte_gravada = fields.Many2one('hr.salary.rule', string='Parte gravada')
    parte_exenta = fields.Many2one('hr.salary.rule', string='Parte exenta')
    cuenta_especie = fields.Many2one('account.account', 'Cuenta de pago', domain=[('deprecated', '=', False)])

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
                   ('problemas_factura', 'Problemas con la factura'), ('factura_cancelada', 'Factura cancelada')],
        string=_('Estado de factura'),
        default='factura_no_generada',
        readonly=False
    )	
    imss_dias = fields.Float('Cotizar en el IMSS',default='15') #, readonly=True) 
    imss_mes = fields.Float('Dias a cotizar en el mes',default='30') #, readonly=True)
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
    concepto_periodico = fields.Boolean('Conceptos periodicos', default = True)

    #imss empleado
    emp_exedente_smg = fields.Float(string='Exedente 3 SMGDF')
    emp_prest_dinero = fields.Float(string='Prest. en dinero')
    emp_esp_pens = fields.Float(string='P. Esp. Desp')
    emp_invalidez_vida = fields.Float( string='Invalidez y Vida')
    emp_cesantia_vejez = fields.Float(string='Cesantia y vejez')
    emp_total = fields.Float(string='IMSS trabajador')
    #imss patronal
    pat_cuota_fija_pat = fields.Float(string='Cuota fija patronal')
    pat_exedente_smg = fields.Float(string='Exedente 3 SMGDF')
    pat_prest_dinero = fields.Float(string='Prest. en dinero')
    pat_esp_pens = fields.Float(string='P. Esp. Desp')
    pat_riesgo_trabajo = fields.Float( string='Riegso de trabajo')
    pat_invalidez_vida = fields.Float( string='Invalidez y Vida')
    pat_guarderias = fields.Float(string='Guarderias y PS')
    pat_retiro = fields.Float( string='Retiro')
    pat_cesantia_vejez = fields.Float(string='Cesantia y vejez')
    pat_infonavit = fields.Float(string='INFONAVIT')
    pat_total = fields.Float(string='IMSS patron')

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
    dias_pagar = fields.Float('Pagar en la nomina')
    no_nomina = fields.Selection(
        selection=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6')], string=_('Nómina del mes'))
    acum_per_totales = fields.Float('Percepciones totales', compute='_get_percepciones_totales')
    acum_per_grav  = fields.Float('Percepciones gravadas', compute='_get_percepciones_gravadas')
    acum_isr  = fields.Float('ISR', compute='_get_isr')
    acum_isr_antes_subem  = fields.Float('ISR antes de SUBEM', compute='_get_isr_antes_subem')
    acum_subsidio_aplicado  = fields.Float('Subsidio aplicado', compute='_get_subsidio_aplicado')
    acum_fondo_ahorro = fields.Float('Fondo ahorro', compute='_get_fondo_ahorro')
    dias_periodo = fields.Float(string=_('Dias en el periodo'), compute='_get_dias_periodo')
    isr_devolver = fields.Boolean(string='Devolver ISR')
    isr_ajustar = fields.Boolean(string='Ajustar ISR en cada nómina')
    acum_sueldo = fields.Float('Sueldo', compute='_get_sueldo')

    mes = fields.Selection(
        selection=[('01', 'Enero'), 
                   ('02', 'Febrero'), 
                   ('03', 'Marzo'),
                   ('04', 'Abril'), 
                   ('05', 'Mayo'),
                   ('06', 'Junio'),
                   ('07', 'Julio'),
                   ('08', 'Agosto'),
                   ('09', 'Septiembre'),
                   ('10', 'Octubre'),
                   ('11', 'Noviembre'),
                   ('12', 'Diciembre'),
                   ],
        string=_('Mes de la nómina'))
    nom_liquidacion = fields.Boolean(string='Nomina de liquidacion', default=False)

    @api.model
    def create(self, vals):
        if not vals.get('fecha_pago') and vals.get('date_to'):
            vals.update({'fecha_pago': vals.get('date_to')})
            
        res = super(HrPayslip, self).create(vals)
        return res
    

    def action_cfdi_nomina_generate(self):
        return True


    def action_cfdi_cancel(self):
        return True

