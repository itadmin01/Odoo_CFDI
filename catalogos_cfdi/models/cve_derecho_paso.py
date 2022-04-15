# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CveDerechoPaso(models.Model):
    _name = 'cve.derecho.paso'
    _rec_name = "clave"

    clave = fields.Char(string='Clave')
    derecho_paso = fields.Char(string='Derecho de paso')