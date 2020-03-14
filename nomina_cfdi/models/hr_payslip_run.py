# -*- coding: utf-8 -*-

from odoo import api, models, fields, _
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from calendar import monthrange
import logging
_logger = logging.getLogger(__name__)

class HrPayslipRun(models.Model):
    _inherit = 'hr.payslip.run'
    
    tipo_configuracion = fields.Many2one('configuracion.nomina', string='Configuración')
    all_payslip_generated = fields.Boolean("Payslip Generated")
    all_payslip_generated_draft = fields.Boolean("Payslip Generated draft")
    tipo_nomina = fields.Selection(
        selection=[('O', 'Nómina ordinaria'), ('E', 'Nómina extraordinaria'),], string=_('Tipo de nómina'), required=True, default='O')
    estructura = fields.Many2one('hr.payroll.structure', string='Estructura')
    tabla_otras_entradas = fields.One2many('otras.entradas', 'form_id')
    dias_pagar = fields.Float(string='Dias a pagar', store=True)
    imss_dias = fields.Float(string='Dias a cotizar en la nómina', store=True)
    imss_mes = fields.Float(string='Dias en el mes', store=True)
    no_nomina = fields.Selection(
        selection=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6')], string=_('No. de nómina en el mes / periodo'))
    nominas_mes = fields.Integer('Nóminas a pagar en el mes')
    concepto_periodico = fields.Boolean('Desactivar conceptos periódicos')
    isr_ajustar = fields.Boolean(string='Ajustar ISR en nómina')
    isr_devolver = fields.Boolean(string='Devolver ISR')
    periodicidad_pago = fields.Selection(
        selection=[('01', 'Diario'), 
                   ('02', 'Semanal'), 
                   ('03', 'Catorcenal'),
                   ('04', 'Quincenal'), 
                   ('05', 'Mensual'),
                   ('06', 'Bimensual'), 
                   ('07', 'Unidad obra'),
                   ('08', 'Comisión'), 
                   ('09', 'Precio alzado'), 
                   ('10', 'Pago por consignación'), 
                   ('99', 'Otra periodicidad'),],
        string=_('Frecuencia de pago'), required=True
    )
        
    def enviar_nomina(self):
        return True
    
    def enviar_prenomina(self):
        return True
    
    def timbrar_nomina(self):
        return True

class OtrasEntradas(models.Model):
    _name = 'otras.entradas'

    form_id = fields.Many2one('hr.payslip.run', required=True) 
    monto = fields.Float('Monto') 
    descripcion = fields.Char('Descripcion') 
    codigo = fields.Char('Codigo')

class ConfiguracionNomina(models.Model):
    _name = 'configuracion.nomina'
    _rec_name = "name"

    name = fields.Char(string='Nombre', required=True)
    tipo_pago = fields.Selection(
        selection=[('01', 'Por periodo'), 
                   ('02', 'Por día'),],
        string=_('Conteo de días'),
    )
    fijo_imss = fields.Boolean(string='Dias fijos')
    imss_dias = fields.Float(string='Dias a cotizar en la nómina', store=True)
    imss_mes = fields.Float(string='Dias en el mes', store=True)
    isr_ajustar = fields.Boolean(string='Ajustar ISR en cada nómina', default= True)
    isr_devolver = fields.Boolean(string='Devolver ISR')
    periodicidad_pago = fields.Selection(
        selection=[('01', 'Diario'), 
                   ('02', 'Semanal'), 
                   ('03', 'Catorcenal'),
                   ('04', 'Quincenal'), 
                   ('05', 'Mensual'),
                   ('06', 'Bimensual'), 
                   ('07', 'Unidad obra'),
                   ('08', 'Comisión'), 
                   ('09', 'Precio alzado'), 
                   ('10', 'Pago por consignación'), 
                   ('99', 'Otra periodicidad'),],
        string=_('Periodicidad de pago CFDI'), required=True
    )
