# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CveCodigoTransporteAereo(models.Model):
    _name = 'cve.codigo.transporte.aereo'
    _rec_name = "aerolinea"

    clave = fields.Char(string='Clave')
    nacionalidad = fields.Char(string='Nacionalidad')
    aerolinea = fields.Char(string='Aerolinea')