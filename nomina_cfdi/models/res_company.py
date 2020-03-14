# -*- coding: utf-8 -*-
import base64
import json
import requests
from odoo import fields, models,api, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta

class ResCompany(models.Model):
    _inherit = 'res.company'

    rfc_patron = fields.Char(string=_('RFC Patrón'))
    serie_nomina = fields.Char(string=_('Serie nomina'))
    registro_patronal = fields.Char(string=_('Registro patronal'))
    #nomina_mail = fields.Many2one("mail.template", 'Nomina Mail',)
    nomina_mail = fields.Char('Nomina Mail',)
