# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CveAurotizacionNaviera(models.Model):
    _name = 'cve.autorizacion.naviera'
    _rec_name = "autorizacion_naviera"

    autorizacion_naviera = fields.Char(string='Número de autorización')
