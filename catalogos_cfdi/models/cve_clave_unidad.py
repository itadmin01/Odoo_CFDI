# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CveClaveUnidad(models.Model):
    _name = 'cve.clave.unidad'
    _rec_name = "nombre"

    clave = fields.Char(string='Clave')
    nombre = fields.Char(string='Nombre')