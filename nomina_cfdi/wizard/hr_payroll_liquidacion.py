# -*- coding: utf-8 -*-

from odoo import models, api, fields,_
from datetime import datetime
from datetime import date

import time
from odoo.exceptions import Warning
import logging
_logger = logging.getLogger(__name__)

class GeneraLiquidaciones(models.TransientModel):
    _name = 'calculo.liquidaciones'

    fecha_inicio = fields.Date(string='Fecha inicio último periodo')
    fecha_liquidacion = fields.Date(string='Fecha liquidacion')
    employee_id =fields.Many2one("hr.employee",'Employee')
    dias_base = fields.Float('Días base', default='90')
    dias_x_ano = fields.Float('Días por cada año trabajado', default='20')
    dias_totales = fields.Float('Total de días', store=True)
    indemnizacion = fields.Boolean("Pagar indemnización")
    antiguedad = fields.Boolean("Pagar antiguedad")
    dias_pendientes_pagar = fields.Float('Días de nómina a pagar', store=True)
    dias_vacaciones = fields.Float('Días de vacaciones')
    dias_aguinaldo = fields.Float('Días aguinaldo')
    dias_prima_vac = fields.Float('Días prima vacacional')
    fondo_ahorro = fields.Float('Fondo ahorro', store=True)
    pago_separacion = fields.Float("Pago por separación")
    contract_id = fields.Many2one('hr.contract', string='Contrato')
    antiguedad_anos = fields.Float('Antiguedad', store=True)

    monto_prima_antiguedad = fields.Float('Prima antiguedad', store=True)
    monto_indemnizacion = fields.Float('Indemnizacion', store=True)
    tipo_de_baja = fields.Selection([('01','Separación voluntaria'),
                                      ('02','Baja')], string='Tipo de baja')
    sueldo_calculo = fields.Selection([('01','Sueldo diario'),
                                      ('02','Sueldo diario integrado')], string='Sueldo para cálculos')
    sueldo_calculo_monto  = fields.Float('Sueldo calculo')
    tope_prima = fields.Selection([('01','Sueldo diario'),
                                      ('02','UMA')], string='Para calculo topado usar')
    tope_prima_monto  = fields.Float('Sueldo calculo')
    estructura  = fields.Many2one('hr.payroll.structure', string='Estructura ordinaria')
    prima_vac = fields.Float('Días aguinaldo')

    def calculo_create(self):
        return True

    def calculo_liquidacion(self):
        return True

    def genera_nominas(self):
        dias_vacaciones = 0

    def get_fondo_ahorro(self):
        return True
