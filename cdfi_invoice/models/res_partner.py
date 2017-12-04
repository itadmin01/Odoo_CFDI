# -*- coding: utf-8 -*-


from odoo import fields, models, api,_


class ResPartner(models.Model):
    _inherit = 'res.partner'

    rfc = fields.Char(string=_('RFC')) 
    banco_emisor = fields.Selection(
                                selection=[ ('BBA940707IE1', 'BANCO DEL BAJIO'),
                                            ('BII931004P61', 'BANCO INBURSA'),
                                            ('BIN931011519', 'BANCO INTERACCIONES'),
                                            ('BMN930209927', 'BANCO MERCANTIL DEL NORTE'),
                                            ('BMI9704113PA', 'BANCO MONEX'),
                                            ('BMI061005NY5', 'BANCO MULTIVA'),
                                            ('BAF950102JP5', 'BANCA AFIRME'),
                                            ('BBA830831LJ2', 'BBVA BANCOMER'),
                                            ('HMI950125KG8', 'HSBC'),
                                            ('IBA950503GTA', 'IXE BANCO'),
                                            ('SIN9412025I4', 'SCOTIABANK INVERLAT'),
                                            ('BSM970519DU8', 'BANCO SANTANDER'),
                                            ('BNM840515VB1', 'BANCO NACIONAL DE MEXICO'),
                                            ('BNE820901682', 'BANCO NACIONAL DE EJERCITO FUERZA AEREA Y ARMADA'),
                                            ('BRM940216EQ6', 'BANCO REGIONAL DE MONTERREY'),
                                            ('BBA130722BR7', 'BANCO BANCREA'),
                                            ('BAI0205236Y8', 'BANCO AZTECA'),],
                                string=_('Banco emisor'),
                            )
    cuenta_emisor = fields.Char("Cuenta del emisor")
    rfc_banco_emisor = fields.Char(_("RFC banco emisor"), compute='_compute_rfc_banco_emisor')
    residencia_fiscal = fields.Char(string=_('Residencia Fiscal'))
    registro_tributario = fields.Char(string=_('Registro tributario'))
            
    @api.one
    @api.depends('banco_emisor')
    def _compute_rfc_banco_emisor(self):
        if self.banco_emisor:
            self.rfc_banco_emisor = self.banco_emisor
    
    