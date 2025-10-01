# coding: utf-8
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResCountry(models.Model):
    _inherit = 'res.country'

    codigo_mx = fields.Char('Código MX', help='Códigos del SAT para los países.')
