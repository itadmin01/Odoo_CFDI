# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CveEstacion(models.Model):
    _name = 'cve.estacion'
    _rec_name = "descripcion"

    c_estacion = fields.Char(string='Clave estacion')
    descripcion = fields.Char(string='Descripción')
    c_transporte = fields.Char(string='Clave transporte')
    fecha_inicio = fields.Date(string='Fecha inicio')