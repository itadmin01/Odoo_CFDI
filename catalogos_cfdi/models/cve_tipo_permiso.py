# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CveTipoPermiso(models.Model):
    _name = 'cve.tipo.permiso'
    _rec_name = "descripcion"

    clave = fields.Char(string='Clave')
    descripcion = fields.Char(string='Descripción')
