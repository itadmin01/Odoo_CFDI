# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Paises(models.Model):
    _name = 'catalogos.paises'
    _rec_name = "descripcion"

    c_pais = fields.Char(string='Clave de Pais')
    descripcion = fields.Char(string='Descripción')
    formato_cp = fields.Char(string='Formato de código postal')
    formato_rit = fields.Char(string='Formato de Registro de Identidad Tributaria')
    validacion_rit = fields.Char(string='Validación del Registro de Identidad Tributaria')
    agrupacion = fields.Char(string='Agrupaciones')