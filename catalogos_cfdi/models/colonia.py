# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Colonia(models.Model):
    _name = 'catalogos.colonias'
    _rec_name = "descripcion"

    c_colonia = fields.Char(string='Clave de Colonia')
    c_codigopostal = fields.Char(string='Código postal')	
    descripcion = fields.Char(string='Descripción')