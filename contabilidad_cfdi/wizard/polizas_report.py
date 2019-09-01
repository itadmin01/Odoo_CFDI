# -*- coding: utf-8 -*-

from odoo import models, fields, api
import requests
import json
from odoo.exceptions import Warning

class PolizasReport(models.TransientModel):
    _name = 'polizas.report'
    
    start_date = fields.Date("Start Date")
    end_date = fields.Date("End Date")
    journal_ids = fields.Many2many('account.journal',string='Journals', default=lambda self: self.env['account.journal'].search([]))
    
    @api.multi
    def action_print_polizas_report(self):
        domain = [('journal_id', 'in',self.journal_ids.ids)]
        if self.start_date:
            domain.append(('date','>=',self.start_date))
        if self.end_date:
            domain.append(('date','<=',self.end_date))
        
        journal_entries = self.env['account.move'].search(domain)
        company = self.env.user.company_id
        request_params = { 
                'company': {
                      'rfc': company.rfc,
                      'api_key': company.proveedor_timbrado,
                      'modo_prueba': company.modo_prueba,
                },
                'informacion':{
                      'proceso': 'polizas',
                      'fecha_inicio': self.start_date or '',
                      'fecha_fin': self.end_date or '',
                },}
        polizas = []
        for move in journal_entries:
            
            mv_vals = {
                'nombre' : move.name,
                'reference' : move.ref or '',
                'diario' : move.journal_id.name,
                'fecha' : move.date,
                }
            transaccion = []
            for line in move.line_ids:
                transaccion.append({
                    'cuenta' : line.account_id.name or '',
                    'codigo' : line.account_id.code or '',
                    'cliente' : line.partner_id.name or '',
                    'label' : line.name or '',
                    'debe' : line.debit,
                    'haber' : line.credit,
                    })
            mv_vals.update({'transaccion' : transaccion})                    
            polizas.append(mv_vals)
        request_params.update({'polizas': polizas})
        
        url=''
        company = self.env.user.company_id
        if company.proveedor_timbrado == 'multifactura':
            url = '%s' % ('http://facturacion.itadmin.com.mx/api/contabilidad')
        elif company.proveedor_timbrado == 'gecoerp':
            if company.modo_prueba:
                url = '%s' % ('https://itadmin.gecoerp.com/invoice/?handler=OdooHandler33')
            else:
                url = '%s' % ('https://itadmin.gecoerp.com/invoice/?handler=OdooHandler33')
        if not url:
            raise Warning("Please setup Proveedor de timbrado on company form.")
        
        response = requests.post(url,auth=None,verify=False, data=json.dumps(request_params),headers={"Content-type": "application/json"})
        json_response = response.json()
        print(json_response)
        return True
    