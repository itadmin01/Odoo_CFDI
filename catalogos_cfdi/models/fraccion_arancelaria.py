# -*- coding: utf-8 -*-

from odoo import models, fields, api

class fraccionarancelaria(models.Model):
    _name = 'catalogos.fraccionarancelaria'
    _rec_name = "c_fraccionarancelaria"

    c_fraccionarancelaria = fields.Char(string='Fraccion Arancelaria')
    descripcion = fields.Char(string='Descripción')