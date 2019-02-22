# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Localidades(models.Model):
    _name = 'catalogos.localidades'
    _rec_name = "descripcion"

    c_localidad = fields.Char(string='Clave de Localidad')
    c_estado = fields.Char(string='Clave Estado')	
    descripcion = fields.Char(string='Descripción')