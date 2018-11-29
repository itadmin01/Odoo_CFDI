# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

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
    tablas_cfdi_id = fields.Many2one('tablas.cfdi','Tabla CFDI')
	
    bono_productividad = fields.Float('Bono productividad')
    bono_asistencia = fields.Float('Bono asistencia')
    bono_puntualidad = fields.Float('Bono puntualidad')
    infonavit_fijo = fields.Float('Infonavit (fijo)')
    infonavit_vsm = fields.Float('Infonavit (vsm)')

    infonavit_porc = fields.Float('Infonavit (%)')
    anticipo_sueldo = fields.Float('Anticipo sueldo')
    deduc_gral = fields.Float('Dedudcion general')
    prestamo_fonacot = fields.Float('Prestamo FONACOT')
    pago_de_serv = fields.Float('Pago de servicio')
    pens_alim = fields.Float('Pensión alimienticia')
    prest_financ = fields.Float('Prestamo financiero')
    prevision_social = fields.Float('Prevision Social')

	
    @api.multi
    @api.onchange('wage')
    def _compute_sueldo(self):
        if self.wage:
            values = {
            'sueldo_diario': self.wage/30,
            'sueldo_hora': self.wage/30/8,
            'sueldo_diario_integrado': self.wage/30*1.0452,
            }
            self.update(values)	

		