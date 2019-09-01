# -*- coding: utf-8 -*-

#from odoo import models, api 

#class AccountInvoice(models.Model):
#    _inherit = 'account.invoice'
    
#    @api.multi
#    def action_cfdi_generate(self):
#        res = super(AccountInvoice, self).action_cfdi_generate()
#        for invoice in self:
#            if invoice.move_id:
#                invoice.move_id.write({'contabilidad_electronica' : True})
#                invoice.move_id.line_ids.write({'contabilidad_electronica' : True})
#        return res