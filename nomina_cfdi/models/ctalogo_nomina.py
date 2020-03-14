# -*- coding: utf-8 -*-

from odoo import models, fields, api

class TipoDeduccion(models.Model):
    _name = 'nomina.deduccion'
    _rec_name = "descripcion"

    clave = fields.Char(string='Clave')
    descripcion = fields.Char(string='Descripción')

class TipoPercepcion(models.Model):
    _name = 'nomina.percepcion'
    _rec_name = "descripcion"

    clave = fields.Char(string='Clave')
    descripcion = fields.Char(string='Descripción')

class TipoOtroPago(models.Model):
    _name = 'nomina.otropago'
    _rec_name = "descripcion"

    clave = fields.Char(string='Clave')
    descripcion = fields.Char(string='Descripción')