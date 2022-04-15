# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CveTipoCarro(models.Model):
    _name = 'cve.tipo.carro'
    _rec_name = "tipo_carro"

    clave = fields.Char(string='Clave')
    tipo_carro = fields.Char(string='Tipo de carro')