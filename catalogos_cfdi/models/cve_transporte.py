# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CveTransporte(models.Model):
    _name = 'cve.transporte'
    _rec_name = "descripcion"

    c_transporte = fields.Char(string='Clave Transporte')
    descripcion = fields.Char(string='Descripción')
