# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError        
    
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

class TablasCFDI(models.Model):
    _name = 'tablas.cfdi'
    
    name = fields.Char("Reference", readonly=True)
    tabla_antiguedades = fields.One2many('tablas.antiguedades.line', 'form_id') 
    tabla_LISR = fields.One2many('tablas.general.line', 'form_id')
    tabla_subem = fields.One2many('tablas.subsidio.line', 'form_id')
    tabla_subsidio = fields.One2many('tablas.subsidio2.line', 'form_id')
    tabla_subsidio_acreditable = fields.One2many('tablas.subsidioacreditable.line', 'form_id')
    uma = fields.Float(string=_('UMA'))
    salario_minimo = fields.Float(string=_('Salario mínimo'))
	
    @api.one
    @api.constrains('name')
    def _check_name(self):
        if self.name:
            if self.search([('id', '!=', self.id),('name','=',self.name)]):
                raise ValidationError(_('Reference with same name already exist.'))
            
    @api.model
    def default_get(self,fields):
        res = super(TablasCFDI,self).default_get(fields)
        if 'name' in fields:
            res['name'] = self.env['ir.sequence'].next_by_code('tablas.cfdi.reference')
        return res   
    