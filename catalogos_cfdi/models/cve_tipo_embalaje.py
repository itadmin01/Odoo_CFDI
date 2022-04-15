# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CveTipoEmbalaje(models.Model):
    _name = 'cve.tipo.embalaje'
    _rec_name = "descripcion"

    clave = fields.Char(string='Clave')
    descripcion = fields.Char(string='Nombre')