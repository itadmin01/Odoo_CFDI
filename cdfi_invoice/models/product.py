# -*- coding: utf-8 -*-
from odoo import fields, models, api,_


    
UM_CLAVO_MAP = {
                'Pieza': 'H87',
                'Hora': 'HUR',
                'Kilogramo': 'KGM',
                'Gramo': 'GRM',
                'Litro': 'LTR',
                'Galon': 'A76',
                'Tonelada': 'TNE',
                'Caja': 'XBX',
                'Metro': 'MTR',
                'Metro lineal': 'LM',
                'M2': 'MTK',
                'M3': 'MTQ',
                'Unidad de servicio': 'E48',
                'Tarifa': 'A9',
                'Dia': 'DAY',
                'Lote': 'XLT',	
                'Conjunto': 'SET',
                'Actividad': 'ACT',
                'Comida': 'Q3',
                'Habitacion': 'ROM',
                'Paquete': 'XPK',
                'Mutuamente definido': 'ZZ',
                'Kit': 'KT',
                }
    
class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    UNIDAD_MEDIDA_LIST=[
                    ('Pieza', 'Pieza'),
                   ('Hora', 'Hora'),
                   ('Kilogramo', 'Kilogramo'),
                   ('Gramo', 'Gramo'),
                   ('Litro', 'Litro'),
                   ('Galon', 'Galon'),
                   ('Tonelada', 'Tonelada'),
                   ('Caja', 'Caja'),
                   ('Metro', 'Metro'),
                   ('Metro lineal', 'Metro lineal'),
                   ('M2', 'M2'),
                   ('M3', 'M3'),
                   ('Unidad de servicio', 'Unidad de servicio'),
                   ('Tarifa', 'Tarifa'),
                   ('Dia', 'Dia'),
                   ('Lote', 'Lote'),
                   ('Conjunto', 'Conjunto'),
                   ('Actividad', 'Actividad'),
                   ('Comida', 'Comida'),				   
                   ('Habitacion', 'Habitacion'),
                   ('Paquete', 'Paquete'),
                   ('Mutuamente definido', 'Mutuamente definido'),
                   ('Kit', 'Kit'),
                   ]
    unidad_medida = fields.Selection(selection=UNIDAD_MEDIDA_LIST, string='Unidad SAT')
    clave_producto = fields.Char(string='Clave producto')
    clave_unidad = fields.Char(string='Clave unidad', compute='_compute_clave_unidad')
    
    @api.depends('unidad_medida')
    @api.one
    def _compute_clave_unidad(self):
        if self.unidad_medida:
            self.clave_unidad = UM_CLAVO_MAP[self.unidad_medida]
            
    