# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime

class TablasAntiguedadesLine(models.Model):
    _name = 'tablas.antiguedades.line'

    form_id = fields.Many2one('tablas.cfdi', string='Vacaciones y aguinaldos', required=True)
    antiguedad = fields.Float('Antigüedad/Años') 
    vacaciones = fields.Float('Vacaciones/Días') 
    prima_vac = fields.Float('Prima vacacional (%)')
    aguinaldo = fields.Float('Aguinaldo/Días')

class TablasGeneralLine(models.Model):
    _name = 'tablas.general.line'

    form_id = fields.Many2one('tablas.cfdi', string='ISR Mensual Art. 113 LISR', required=True)
    lim_inf = fields.Float('Límite inferior') 
    c_fija = fields.Float('Cuota fija') 
    s_excedente = fields.Float('Sobre excedente (%)')

class TablasSubsidiolLine(models.Model):
    _name = 'tablas.subsidio.line'

    form_id = fields.Many2one('tablas.cfdi', string='Subem mensual/CAS Mensual', required=True)
    lim_inf = fields.Float('Límite inferior') 
    s_mensual = fields.Float('Subsidio mensual')

class TablasSubsidio2lLine(models.Model):
    _name = 'tablas.subsidio2.line'

    form_id = fields.Many2one('tablas.cfdi', string='Subsidio Mensual Art. 114 LISR', required=True)
    lim_inf = fields.Float('Límite inferior') 
    c_fija = fields.Float('Cuota fija') 
    s_imp_marginal = fields.Float('Sobre imp. marginal (%)')

class TablasSubsidioAcreditablelLine(models.Model):
    _name = 'tablas.subsidioacreditable.line'

    form_id = fields.Many2one('tablas.cfdi', string='Subsidio acreditable', required=True)
    ano = fields.Float('Año') 
    s_mensual = fields.Float('Subsidio (%)')

class TablasPeriodoBimestrallLine(models.Model):
    _name = 'tablas.periodo.bimestral'

    form_id = fields.Many2one('tablas.cfdi', string='Periodo bimestral', required=True)
    dia_inicio = fields.Date('Primer día del peridoo') 
    dia_fin = fields.Date('Ultímo día del peridoo') 
    no_dias = fields.Float('Dias en el periodo', store=True)


class TablasPeriodoMensuallLine(models.Model):
    _name = 'tablas.periodo.mensual'

    form_id = fields.Many2one('tablas.cfdi', string='Periodo mensual', required=True)
    dia_inicio = fields.Date('Primer día del peridoo') 
    dia_fin = fields.Date('Ultímo día del peridoo') 
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
        string=_('Mes'),)
    no_dias = fields.Float('Dias en el mes', store=True) 
  

class TablasPeriodoSemanalLine(models.Model):
    _name = 'tablas.periodo.semanal'

    form_id = fields.Many2one('tablas.cfdi', string='Calendario semanal', required=True)
    no_periodo = fields.Integer('No. periodo')
    dia_inicio = fields.Date('Primer día del peridoo') 
    dia_fin = fields.Date('Ultímo día del peridoo') 
    no_dias = fields.Float('Dias en el periodo', store=True)



class TablasAnualISR(models.Model):
    _name = 'tablas.isr.anual'

    form_id = fields.Many2one('tablas.cfdi', string='ISR Anual', required=True)
    lim_inf = fields.Float('Límite inferior') 
    c_fija = fields.Float('Cuota fija') 
    s_excedente = fields.Float('Sobre excedente (%)')


class TablasCFDI(models.Model):
    _name = 'tablas.cfdi'
    
    name = fields.Char("Nombre")
    tabla_antiguedades = fields.One2many('tablas.antiguedades.line', 'form_id', copy=True) 
    tabla_LISR = fields.One2many('tablas.general.line', 'form_id', copy=True)
    tabla_ISR_anual = fields.One2many('tablas.isr.anual', 'form_id', copy=True)
    tabla_subem = fields.One2many('tablas.subsidio.line', 'form_id', copy=True)
    tabla_subsidio = fields.One2many('tablas.subsidio2.line', 'form_id', copy=True)
    tabla_subsidio_acreditable = fields.One2many('tablas.subsidioacreditable.line', 'form_id', copy=True)
    tabla_bimestral = fields.One2many('tablas.periodo.bimestral', 'form_id', copy=True)
    tabla_mensual = fields.One2many('tablas.periodo.mensual', 'form_id', copy=True)
    tabla_semanal = fields.One2many('tablas.periodo.semanal', 'form_id', copy=True)

    uma = fields.Float(string=_('UMA'), default='84.49')
    salario_minimo = fields.Float(string=_('Salario mínimo'))
    imss_mes = fields.Float('Periodo mensual nómina (dias)',default='30.4')
	
    importe_utilidades = fields.Float(string=_('Importe a repartir a todos los empleados'), default=0)
    dias_min_trabajados = fields.Float(string=_('Dias mínimos trabajados en empleados eventuales'), default=60)
    funcion_ingresos = fields.Float(string=_('% a repartir en función de los ingresos'), default=50)
    funcion_dias = fields.Float(string=_('% a repartir en función de los días trabajados'), readonly=True)
    total_dias_trabajados = fields.Float(string=_('Total de días trabajados'), default=0)
    total_sueldo_percibido = fields.Float(string=_('Total de sueldo percibido'), default=0)
    factor_dias = fields.Float(string=_('Factor por dias trabajados'), readonly=True)
    factor_sueldo = fields.Float(string=_('Factor por sueldo percibido'), readonly=True)
    fecha_inicio = fields.Date('Fecha inicio')
    fecha_fin = fields.Date('Fecha fin')

    ######## Variables del seguro ####################3
    apotacion_infonavit = fields.Float(string=_('Aportación al Infonavit (%)'), default=5, digits = (12,3))
    umi = fields.Float(string=_('UMI (Unidad Mixta INFONAVIT)'), default=82.22, digits = (12,3))
    sbcm_general = fields.Float(string=_('General (UMA)'), default=25, digits = (12,3))
    sbcm_inv_inf = fields.Float(string=_('Para invalidez e Infonavit (UMA)'), default=25, digits = (12,3))
    rt_clase1 = fields.Float(string=_('Clase 1'), default=0.55456, digits = (12,6))
    rt_clase2 = fields.Float(string=_('Clase 2'), default=1.130658, digits = (12,6))
    rt_clase3 = fields.Float(string=_('Clase 3'), default=2.59844, digits = (12,6))
    rt_clase4 = fields.Float(string=_('Clase 4'), default=4.65325, digits = (12,6))
    rt_clase5 = fields.Float(string=_('Clase 5'), default=7.58875, digits = (12,6))
    enf_mat_cuota_fija = fields.Float(string=_('Cuota fija (%)'), default=20.4, digits = (12,3))
    enf_mat_excedente_p = fields.Float(string=_('Excedente de 3 UMA (%)'), default=1.10, digits = (12,3))
    enf_mat_excedente_e = fields.Float(string=_('Excedente de 3 UMA (%)'), default=0.40, digits = (12,3))

    enf_mat_prestaciones_p = fields.Float(string=_('Prestaciones en dinero (%)'), default=0.7, digits = (12,3))
    enf_mat_prestaciones_e = fields.Float(string=_('Prestaciones en dinero (%)'), default=0.25, digits = (12,3))
    enf_mat_gastos_med_p = fields.Float(string=_('Gastos médicos personales (%)'), default=1.05, digits = (12,3))
    enf_mat_gastos_med_e = fields.Float(string=_('Gastos médicos personales (%)'), default=0.375, digits = (12,3))

    inv_vida_p = fields.Float(string=_('Invalidez y vida (%)'), default=1.75, digits = (12,3))
    inv_vida_e = fields.Float(string=_('Invalidez y vida (%)'), default=0.625, digits = (12,3))

    cesantia_vejez_p = fields.Float(string=_('Cesantía y vejez (%)'), default=3.15, digits = (12,3))
    cesantia_vejez_e = fields.Float(string=_('Cesantía y vejez (%)'), default=1.125, digits = (12,3))

    retiro_p = fields.Float(string=_('Retiro (%)'), default=2, digits = (12,3))
    guarderia_p = fields.Float(string=_('Guardería y prestaciones sociales (%)'), default=1, digits = (12,3))

    @api.constrains('name')
    def _check_name(self):
        if self.name:
            if self.search([('id', '!=', self.id),('name','=',self.name)]):
                raise ValidationError(_('Reference with same name already exist.'))
            
    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        default = dict(default or {})
        default.setdefault('name', _("%s (copy)") % (self.name or ''))
        return super(TablasCFDI, self).copy(default)
    
    @api.model
    def default_get(self,fields):
        res = super(TablasCFDI,self).default_get(fields)
        if 'name' in fields:
            res['name'] = self.env['ir.sequence'].next_by_code('tablas.cfdi.reference')
        return res

    def calcular_reparto_utilidades(self):
        return True

    def button_dummy(self):
        self.calcular_reparto_utilidades()
        return True