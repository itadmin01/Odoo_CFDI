# -*- coding: utf-8 -*-
from odoo import fields, models, api,_

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    cat_unidad_medida  =  fields.Many2one('catalogo.unidad.medida', string='Unidad SAT')
    clave_producto = fields.Char(string='Clave producto')
    objetoimp = fields.Selection(
        selection=[('01', 'No objeto de impuesto'),
                   ('02', 'Sí objeto de impuesto'),
                   ('03', 'Sí objeto del impuesto y no obligado al desglose'),
                   ('04', 'Si objeto del impuesto y no causa impuesto'),],
        string=_('Impuestos'),
    )
    product_parts_ids = fields.One2many('product.parts','parent_line_id',string='Partes')
    company_cfdi = fields.Boolean(string='Compania CFDI', compute='_get_company')

    @api.depends('company_id')
    def _get_company(self):
        for record in self:
            if record.company_id:
               record.company_cfdi = record.company_id.company_cfdi
            else:
               record.company_cfdi = True

class ProductComponents(models.Model):
    _name = "product.parts"

    parent_line_id = fields.Many2one('product.template',string="Productos padre ID")
    product_id = fields.Many2one('product.product', string="Partes")
    cantidad = fields.Float(string="Cantidad")
