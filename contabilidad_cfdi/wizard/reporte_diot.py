# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
import calendar

class ReporteDIOTWizard(models.TransientModel):
    _name = 'reporte.diot.wizard'
    
    year = fields.Selection([('2019','2019'), ('2018','2018'), ('2017','2017')], string="Año", required=1)
    month = fields.Selection([('01','Enero'),('02','Febrero'),('03','Marzo'),('04','Abril'),('05','Mayo'),('06','Junio'),('07','Julio'),('08','Agosto'),('09','Septiembre'),('10','Octubre'),('11', 'Noviembre'),('12','Diciembre')], string='Mes', required=1)
    
    @api.multi
    def action_view_report(self):
        date_from = self.year+'-'+self.month+'-01'
        date_to = self.year+'-'+self.month+'-'+str(calendar.monthrange(int(self.year),int(self.month))[1])
        
        move_lines = self.env['account.move.line'].search([('journal_id.type','=', 'purchase'),
                                                           ('date', '>=',date_from), 
                                                           ('date', '<=',date_to),
                                                           ('tax_ids','!=', False),
                                                           ('tax_ids.amount','in', [16.0,8.0,0.0]),
                                                           ])
        
        line_vals = {}
        for line in move_lines:
            partner = line.partner_id
            partner_id = partner.id
            if partner_id not in line_vals:
                line_vals[partner_id] = {
                                         'tipo_proveedor' : partner.tipo_proveedor,
                                         'tipo_operacion' : partner.tipo_operacion,
                                         'rfc' : partner.rfc,
                                         'registro_tributario' : partner.registro_tributario,
                                         'partner_id' : partner_id,
                                         'residencia_fiscal' : partner.residencia_fiscal
                                         }
            
            if line.tax_ids.filtered(lambda x: x.amount==16.0) and partner.rfc != 'XEXX010101000':
                line_vals[partner_id].update({'pagado_16_amount': line.debit + line.credit + line_vals[partner_id].get('pagado_16_amount',0)})
            elif line.tax_ids.filtered(lambda x: x.amount==8.0):
                line_vals[partner_id].update({'pagado_8_amount': line.debit + line.credit + line_vals[partner_id].get('pagado_8_amount',0)})
            elif line.tax_ids.filtered(lambda x: x.amount==0.0) and line.tax_ids.filtered(lambda x: x.tipo_factor != 'Exento'):
                line_vals[partner_id].update({'pagado_0_amount': line.debit + line.credit + line_vals[partner_id].get('pagado_0_amount',0)})
            elif line.tax_ids.filtered(lambda x: x.amount==16.0) and partner.rfc == 'XEXX010101000':
                line_vals[partner_id].update({'importacion_16': line.debit + line.credit + line_vals[partner_id].get('importacion_16',0)})
            elif line.tax_ids.filtered(lambda x: x.amount==0.0) and line.tax_ids.filtered(lambda x: x.tipo_factor == 'Exento'):
                line_vals[partner_id].update({'exento': line.debit + line.credit + line_vals[partner_id].get('exento',0)})
                
#             if line.tax_ids.amount==16.0 and partner.rfc != 'XEXX010101000':
#                 line_vals[partner_id].update({'pagado_16_amount': line.debit + line.credit + line_vals[partner_id].get('pagado_16_amount',0)})
#             elif line.tax_ids.amount==8.0:
#                 line_vals[partner_id].update({'pagado_8_amount': line.debit + line.credit + line_vals[partner_id].get('pagado_8_amount',0)})
#             elif line.tax_ids.amount==0.0 and line.tax_ids.tipo_factor != 'Exento' :
#                 line_vals[partner_id].update({'pagado_0_amount': line.debit + line.credit + line_vals[partner_id].get('pagado_0_amount',0)})
#             elif line.tax_ids.amount==16.0 and partner.rfc == 'XEXX010101000':
#                 line_vals[partner_id].update({'importacion_16': line.debit + line.credit + line_vals[partner_id].get('importacion_16',0)})
#             elif line.tax_ids.amount==0.0 and line.tax_ids.tipo_factor == 'Exento' :
#                 line_vals[partner_id].update({'exento': line.debit + line.credit + line_vals[partner_id].get('exento',0)})

        wizard_line_obj = self.env['reporte.diot.wizard.line']
        created_lines = []
        for partner_id,vals in line_vals.items():
            rec = wizard_line_obj.create(vals)
            created_lines.append(rec.id)
        
        try:
            tree_id = self.env['ir.model.data'].get_object_reference('contabilidad_cfdi', 'reporte_diot_wizard_line_form_view_tree_itadmin')[1]
        except ValueError:
            tree_id = False
            
        return {
            'name': 'Reporte DIOT',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'reporte.diot.wizard.line',
            'views': [(tree_id, 'tree')],
            'view_id': tree_id,
            'domain': [('id','in',created_lines)]
        }    
        


class ReporteDIOTWizardLine(models.TransientModel):
    _name = 'reporte.diot.wizard.line'
    
    tipo_proveedor = fields.Selection(
        selection=[('04', _('04 - Proveedor nacional')),
                   ('05', _('05 - Proveedor extranjero')),
                   ('15', _('15 - Proveedor global')),],string=_('Tipo de tercero'),)
    
    tipo_operacion = fields.Selection(
        selection=[('03', _('03 - Provisión de servicios profesionales')),
                   ('06', _('06 - Arrendamientos')),
                   ('85', _('85 - Otros')),],
        string=_('Tipo de opreacion'),
    )
    rfc = fields.Char("RFC")
    registro_tributario = fields.Char(string='No. ID fiscal')
    partner_id = fields.Many2one('res.partner',string='Nombre')
    residencia_fiscal = fields.Char(string='Nacionalidad')
    pagado_16_amount = fields.Float('Pagado 16%')
    pagado_16_amount_no_acreditable = fields.Float('Pagado 16% no acreditable')
    pagado_8_amount = fields.Float('Pagado 8%')
    pagado_8_amount_no_acreditable = fields.Float('Pagado 8% no acreditable')
    importacion_16 = fields.Float('Importacion 16%')
    pagado_0_amount = fields.Float('Pagado 0%')
    exento = fields.Float('Exento')
