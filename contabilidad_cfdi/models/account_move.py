# -*- coding: utf-8 -*-

from odoo import fields, models

class AccountMove(models.Model):
    _inherit = 'account.move'
        
    contabilidad_electronica = fields.Boolean('CE', copy=False, readonly=True)
    account_cfdi_ids = fields.One2many('account.move.cfdi33','move_id', 'CFDI 3.3')
    
    
class AccountMoveCFDI33(models.Model):
    _name = 'account.move.cfdi33'
    
    fecha = fields.Date('Fecha')
    folio = fields.Char('Folio')
    uuid = fields.Char('UUID')
    partner_id = fields.Many2one('res.partner','Cliente')
    monto = fields.Float('Monto')
    move_id = fields.Many2one('account.move', 'Move')