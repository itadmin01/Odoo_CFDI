# -*- coding: utf-8 -*-

from odoo import models, api, fields, _
from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
import time
    
class GeneraLiquidaciones(models.TransientModel):
    _name = 'calculo.liquidaciones'
    
    

    fecha_inicio = fields.Date(string='Fecha ultimo periodo nómina')
    fecha_liquidacion = fields.Date(string='Fecha liquidacion')
    employee_id =fields.Many2one("hr.employee",'Employee')
    dias_base = fields.Float('Días base', default='90')
    dias_x_ano = fields.Float('Días por cada año trabajado', default='20')
    dias_totales = fields.Float('Total de días', readonly=True, store=True)
    indemnizacion = fields.Boolean("Indemnizar al empleado")
    dias_pendientes_pagar = fields.Float('Días a pagar', readonly=True, store=True)
    dias_vacaciones = fields.Integer('Días de vacaciones')
    dias_aguinaldo = fields.Integer('Días aguinaldo')
    fondo_ahorro = fields.Float('Fondo ahorro', compute="get_fondo_ahorro", store=True)
    prima_vacacional = fields.Boolean("Prima vacacional pendiente")
    pago_separacion = fields.Float("Pago por separación")
    contract_id = fields.Many2one('hr.contract', string='Contrato')
    antiguedad_anos = fields.Float('Antiguedad', readonly=True, store=True)
    
    year_date_start = fields.Date("Año de inicio")
    number_date_start = fields.Integer("Año de inicio")
    year = fields.Date("Año actual")
    actual_year = fields.Integer("Año actual")
    first_day_date = fields.Date("First day date")
    testing = fields.Integer("TESTING")

   




    monto_prima_antiguedad = fields.Float('Prima antiguedad',readonly=True, store=True)
    monto_indemnizacion = fields.Float('Indemnizacion',readonly=True, store=True)

    @api.multi
    def calculo_liquidacion(self):
        if self.employee_id and self.contract_id:
        #cálculo de conceptos de nómina extraordinaria
           self.antiguedad_anos = self.contract_id.antiguedad_anos
           #calculo de dias a indemnizar
           if self.indemnizacion:
                self.dias_totales = self.contract_id.antiguedad_anos * self.dias_x_ano + self.dias_base
           else:
                self.dias_totales = 0
           self.monto_indemnizacion = self.dias_totales * self.contract_id.sueldo_diario

           # calculo prima antiguedad: 12 días de salario por cada año de servicio.
           self.monto_prima_antiguedad = self.contract_id.antiguedad_anos * 12 * self.contract_id.sueldo_diario

        #cálculo de conceptos de nómina ordinaria
           #dias pendientes a pagar en ultima nomina
           #delta_dias  = datetime.strptime(self.fecha_inicio,"%Y-%m-%d") - datetime.strptime(self.fecha_liquidacion,"%Y-%m-%d")
           #delta_dias  = datetime.strptime(self.fecha_inicio,"%Y,%m,%d") - datetime.strptime(self.fecha_liquidacion,"%Y,%m,%d")
           date_format = "%Y-%m-%d"
           a = self.fecha_inicio
           b = self.fecha_liquidacion
           delta = b - a
           #f_inicio = date(self.fecha_inicio,"%Y, %m, %d")
           #f_final = date(self.fecha_liquidacion,"%Y, %m, %d")
           #delta_dias = (f_inicio - f_final)
           #Ya funciona :O
           self.dias_pendientes_pagar = delta.days


           #Esto saca el año en integer de la fecha en que empezo a trabajar

           year_date_start = datetime.strptime(self.contract_id.date_start, date_format)
           self.number_date_start = year_date_start.year

           #Esto saca el año en integer actual
           year, month, day, hour, minute = time.strftime("%Y,%m,%d,%H,%M").split(',') 
           self.actual_year = year

           self.first_day_date = date(date.today().year, 1, 1)
           self.dias_vacaciones = sum([r.dias for r in self.contract_id.tabla_vacaciones])


           #Función para saber los dias de aguinaldo si el año es anterior al actual
           if self.number_date_start < self.actual_year:
               date_format = "%Y-%m-%d"
               c=datetime.strptime(self.fecha_liquidacion, date_format)
               d=datetime.strptime(self.first_day_date, date_format)

               delta1 = c-d
               self.dias_aguinaldo = delta1.days
               
           #Función para saber los dias de aguinaldo si el año es el actual
           else:
               date_format = "%Y-%m-%d"
               e=datetime.strptime(self.fecha_liquidacion, date_format)
               f=datetime.strptime(self.contract_id.date_start, date_format)
               delta2 = e-f
               self.dias_aguinaldo = delta2.days
    
           #fondo de ahorro (si hay)
          # fondo_ahorr = get_fondo_ahorro()


          
    
           




           #prima vacacional liquidacion
           
        return {
            "type": "ir.actions.do_nothing",
        }


    @api.multi
    def genera_nominas(self):
        dias_vacaciones = 0

    def get_fondo_ahorro(self):
        total = 0
        if self.employee_id and self.mes and self.contract_id.tablas_cfdi_id:
            mes_actual = self.env['tablas.periodo.mensual'].search([('mes', '=', self.mes)])[0]
            date_start = mes_actual.dia_inicio # self.date_from
            date_end = mes_actual.dia_fin #self.date_to
            domain=[('state','=', 'done')]
            if date_start:
                domain.append(('date_from','>=',date_start))
            if date_end:
                domain.append(('date_to','<=',date_end))
            domain.append(('employee_id','=',self.employee_id.id))
            rules = self.env['hr.salary.rule'].search([('code', '=', 'D067')])
            payslips = self.env['hr.payslip'].search(domain)
            payslip_lines = payslips.mapped('line_ids').filtered(lambda x: x.salary_rule_id.id in rules.ids)
            employees = {}
            for line in payslip_lines:
                 if line.slip_id.employee_id not in employees:
                     employees[line.slip_id.employee_id] = {line.slip_id: []}
                 if line.slip_id not in employees[line.slip_id.employee_id]:
                     employees[line.slip_id.employee_id].update({line.slip_id: []})
                 employees[line.slip_id.employee_id][line.slip_id].append(line)

            for employee, payslips in employees.items():
                for payslip,lines in payslips.items():
                    for line in lines:
                        total += line.total
        return total