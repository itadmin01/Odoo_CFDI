# -*- coding: utf-8 -*-
import logging
from odoo import api, fields, models, _
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
    tablas_cfdi_id = fields.Many2one('tablas.cfdi','Tabla CFDI')

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
    
#    @api.onchange('tablas_cfdi_id','wage')
#    def _compute_values(self):
#        if self.tablas_cfdi_id:
#            line = self.env['tablas.general.line'].search([('form_id','=',self.tablas_cfdi_id.id),('lim_inf','<=',self.wage)],order='lim_inf desc',limit=1)
#            if line:
#                limite_inferior = line.lim_inf
#                cuota_fija = line.c_fija
#                sueldo_excedente = line.s_excedente
#                _logger.info('limite_inferior ... %s ', limite_inferior)
#                _logger.info('cuota_fija ... %s ', cuota_fija)
#                _logger.info('sueldo_excedente ... %s ', sueldo_excedente)
		