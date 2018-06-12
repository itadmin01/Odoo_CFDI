# -*- coding: utf-8 -*-

from odoo import fields, models, api,_

class ResCompany(models.Model):
    _inherit = 'res.company'

    rfc_patron = fields.Char(string=_('RFC Patrón'))
    serie_nomina = fields.Char(string=_('Serie nomina'))
    registro_patronal = fields.Char(string=_('Registro patronal'))