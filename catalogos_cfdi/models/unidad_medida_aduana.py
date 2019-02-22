# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Unidadmedidaaduana(models.Model):
    _name = 'catalogos.unidadmedidaaduana'
    _rec_name = "descripcion"

    c_unidadmedidaaduana = fields.Char(string='Unidad Medida Aduana')
    descripcion = fields.Char(string='Descripción')