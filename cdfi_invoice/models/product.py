# -*- coding: utf-8 -*-
from odoo import fields, models, api,_

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    cat_unidad_medida  =  fields.Many2one('catalogo.unidad.medida', string='Unidad SAT')
    clave_producto = fields.Char(string='Clave producto')
