# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CveTipoCarga(models.Model):
    _name = 'cve.tipo.carga'
    _rec_name = "descripcion"

    clave = fields.Char(string='Clave')
    descripcion = fields.Char(string='Descripción')