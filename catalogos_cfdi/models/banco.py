# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Banco(models.Model):
    _name = 'catalogos.banco'
    _rec_name = "descripcion"

    c_banco = fields.Char(string='Clave de Banco')
    descripcion = fields.Char(string='Descripción')