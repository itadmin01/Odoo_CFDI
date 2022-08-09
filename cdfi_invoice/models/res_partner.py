# -*- coding: utf-8 -*-

from odoo import fields, models, _

class ResPartner(models.Model):
    _inherit = 'res.partner'

    residencia_fiscal = fields.Char(string=_('Residencia Fiscal'))
    registro_tributario = fields.Char(string=_('Registro tributario'))
    uso_cfdi_id  =  fields.Many2one('catalogo.uso.cfdi', string='Uso CFDI (cliente)')
    regimen_fiscal_id  =  fields.Many2one('catalogo.regimen.fiscal', string='Régimen Fiscal')

#    def check_vat(self):
#        if self.env.context.get('company_id'):
#            company = self.env['res.company'].browse(self.env.context['company_id'])
#        else:
#            company = self.env.company
#        if company.vat_check_vies:
            # force full VIES online check
#            check_func = self.vies_vat_check
#        else:
            # quick and partial off-line checksum validation
#            check_func = self.simple_vat_check
#        for partner in self:
#            if not partner.vat:
#                continue
            #check with country code as prefix of the TIN
#            vat_country, vat_number = self._split_vat(partner.vat)
#            if not check_func(vat_country, vat_number):
                #if fails, check with country code from country
#                country_code = 'MX' #partner.commercial_partner_id.country_id.code
#                if country_code:
#                    if not check_func(country_code.lower(), partner.vat):
#                        msg = partner._construct_constraint_msg(country_code.lower())
#                        raise ValidationError(msg)
