# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
#import datetime
from datetime import datetime, timedelta
import logging
_logger = logging.getLogger(__name__)

class Contract(models.Model):
    _inherit = "hr.contract"
    
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
        string=_('Periodicidad de pago CFDI'),
    )

    riesgo_puesto = fields.Selection(
        selection=[('1', 'Clase I'), 
                   ('2', 'Clase II'), 
                   ('3', 'Clase III'),
                   ('4', 'Clase IV'), 
                   ('5', 'Clase V'), 
                   ('99', 'No aplica'),],
        string=_('Riesgo del puesto'),
    )	
    sueldo_diario = fields.Float('Sueldo diario')
    sueldo_hora = fields.Float('Sueldo por hora')
    sueldo_diario_integrado = fields.Float('Sueldo diario integrado')
    sueldo_base_cotizacion = fields.Float('Sueldo base cotización (IMSS)')
    tablas_cfdi_id = fields.Many2one('tablas.cfdi','Tabla CFDI')

    bono_productividad = fields.Boolean('Bono productividad')
    bono_productividad_amount = fields.Float('Bono productividad')
    bono_asistencia = fields.Boolean('Bono asistencia')
    bono_asistencia_amount = fields.Float('Monto bono asistencia')
    bono_puntualidad = fields.Boolean('Bono puntualidad')
    bono_puntualidad_amount = fields.Float('Monto bono puntualidad')
    fondo_ahorro  = fields.Boolean('Fondo de ahorro')
    fondo_ahorro_amount  = fields.Float('Monto fondo de ahorro')
    vale_despensa  = fields.Boolean('Vale de despensa')
    vale_despensa_amount  = fields.Float('Monto vale de despensa')
    alimentacion  = fields.Boolean('Alimentación')
    alimentacion_amount  = fields.Float('Monto alimentación')
    percepcion_adicional  = fields.Boolean('Percepcion adicional')
    percepcion_adicional_amount  = fields.Float('Monto percepcion adicional')
	
    infonavit_fijo = fields.Float(string=_('Infonavit (fijo)'), digits = (12,4))
    infonavit_vsm = fields.Float(string=_('Infonavit (vsm)'), digits = (12,4))
    infonavit_porc = fields.Float(string=_('Infonavit (%)'), digits = (12,4))
    prestamo_fonacot = fields.Float('Prestamo FONACOT')
    pens_alim = fields.Float('Pensión alimienticia (%)')
    caja_ahorro  = fields.Boolean('Caja de ahorro')
    caja_ahorro_amount  = fields.Float('Monto caja de ahorro')
    deduccion_adicional  = fields.Boolean('Deduccion adicional')
    deduccion_adicional_amount  = fields.Float('Monto deduccion adicional')
	
    antiguedad_anos = fields.Float('Años de antiguedad')

    tabla_vacaciones = fields.One2many('tablas.vacaciones.line', 'form_id') 
    tipo_pago = fields.Selection(
        selection=[('01', 'Por periodo'), 
                   ('02', 'Por día'),
                   ('03', 'Mes proporcional'),],
        string=_('Conteo de días'),
    )
    tipo_prima_vacacional = fields.Selection(
        selection=[('01', 'Al cumplir el año'), 
                   ('02', 'Con día de vacaciones'),],
        string=_('Prima vacacional'),
        default = '02'
    )
    septimo_dia = fields.Boolean(string='Falta proporcional septimo día')
    incapa_sept_dia = fields.Boolean(string='Incapacidad para cálculo 7mo día')
    sept_dia = fields.Boolean(string='Séptimo día separado')
    semana_inglesa = fields.Boolean(string='Semana inglesa')
    prima_dominical = fields.Boolean(string='Prima dominical')


    def button_dummy(self):
        return True
    
    @api.model
    def calculate_sueldo_base_cotizacion(self): 
        return 0

    @api.model
    def calculate_sueldo_diario_integrado(self): 
        return 0


class TablasVacacioneslLine(models.Model):
    _name = 'tablas.vacaciones.line'

    form_id = fields.Many2one('hr.contract', string='Vacaciones', required=True)
    dias = fields.Integer('Dias disponibles') 
    ano = fields.Selection(
        selection=[('2018', '2018'),
                   ('2019', '2019'),
                   ('2020', '2020'),
                   ('2021', '2021'),
                   ],
        string=_('Año'),)