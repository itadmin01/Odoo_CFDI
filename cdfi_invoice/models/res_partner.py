# -*- coding: utf-8 -*-


from odoo import fields, models, api,_


class ResPartner(models.Model):
    _inherit = 'res.partner'

    rfc = fields.Char(string=_('RFC')) 
    residencia_fiscal = fields.Char(string=_('Residencia Fiscal'))
    registro_tributario = fields.Char(string=_('Registro tributario'))
