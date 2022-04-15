# -*- coding: utf-8 -*-
from odoo import fields, models, api,_

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    cat_unidad_medida  =  fields.Many2one('catalogo.unidad.medida', string='Unidad SAT')
    clave_producto = fields.Char(string='Clave producto')
    objetoimp = fields.Selection(
        selection=[('01', 'No objeto de impuesto'), 
                   ('02', 'Sí objeto de impuesto'), 
                   ('03', 'Sí objeto del impuesto y no obligado al desglose'),],
        string=_('Impuestos'), default = '02',
    )
