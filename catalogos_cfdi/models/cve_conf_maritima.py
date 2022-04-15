# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CveConfMaritima(models.Model):
    _name = 'cve.conf.maritima'
    _rec_name = "clave"

    clave = fields.Char(string='Clave')
    descripcion = fields.Char(string='Descripción')
