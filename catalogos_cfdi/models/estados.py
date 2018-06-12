# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Estado(models.Model):
    _name = 'catalogos.estados'
    _rec_name = "descripcion"

    c_estado = fields.Char(string='Clave de Estado')
    c_pais = fields.Char(string='Clave País')	
    descripcion = fields.Char(string='Descripción')