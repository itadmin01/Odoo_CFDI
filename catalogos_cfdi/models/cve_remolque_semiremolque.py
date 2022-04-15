# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CveRemolqueSemiremolque(models.Model):
    _name = 'cve.remolque.semiremolque'
    _rec_name = "descripcion"

    clave = fields.Char(string='Clave')
    descripcion = fields.Char(string='Descripción')