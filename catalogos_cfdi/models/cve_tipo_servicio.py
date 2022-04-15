# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CveTipoServicio(models.Model):
    _name = 'cve.tipo.servicio'
    _rec_name = "descripcion"

    clave = fields.Char(string='Clave')
    descripcion = fields.Char(string='Descripción')
