# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ClaveUnidad(models.Model):
    _name = 'catalogos.clave_unidad'
    _rec_name = 'nombre'

    c_claveunidad = fields.Char(string="Clave de Unidad", required=True)
    nombre = fields.Char()
