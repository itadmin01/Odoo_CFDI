# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CveMaterialPeligroso(models.Model):
    _name = 'cve.material.peligroso'
    _rec_name = "descripcion"

    clave = fields.Char(string='Clave')
    descripcion = fields.Char(string='Descripción')