# -*- coding: utf-8 -*-

from odoo import api, models, fields, _

class HrPayslipRun(models.Model):
    _inherit = 'hr.payslip.run'
    
    all_payslip_generated = fields.Boolean("Payslip Generated",compute='_compute_payslip_cgdi_generated')
    tipo_nomina = fields.Selection(
        selection=[('O', 'Nómina ordinaria'), ('E', 'Nómina extraordinaria'),], string=_('Tipo de nómina'), required=True, default='O')
    estructura = fields.Many2one('hr.payroll.structure', string='Estructura')
    tabla_otras_entradas = fields.One2many('otras.entradas', 'form_id')

    @api.one
    @api.depends('slip_ids.state','slip_ids.nomina_cfdi')
    def _compute_payslip_cgdi_generated(self):
        cfdi_generated = True
        for payslip in self.slip_ids:
            if payslip.state in ['draft','verify']  or not payslip.nomina_cfdi:
                cfdi_generated=False
                break
        self.all_payslip_generated = cfdi_generated 
        
    @api.multi
    def enviar_nomina(self):
        self.ensure_one()
        ctx = self._context.copy()
        template = self.env.ref('nomina_cfdi.email_template_payroll', False)
        for payslip in self.slip_ids: 
            ctx.update({
                'default_model': 'hr.payslip',
                'default_res_id': payslip.id,
                'default_use_template': bool(template),
                'default_template_id': template.id,
                'default_composition_mode': 'comment',
            })
            
            vals = self.env['mail.compose.message'].onchange_template_id(template.id, 'comment', 'hr.payslip', payslip.id)
            mail_message  = self.env['mail.compose.message'].with_context(ctx).create(vals.get('value',{}))
            mail_message.send_mail_action()
        return True
    
    @api.multi
    def timbrar_nomina(self):
        self.ensure_one()
        cr = self._cr
        payslip_obj = self.env['hr.payslip']
        for payslip_id in self.slip_ids.ids:
            try:
                cr.execute('SAVEPOINT model_payslip_confirm_cfdi_save')
                payslip = payslip_obj.browse(payslip_id)
                if payslip.state in ['draft','verify']:
                    payslip.action_payslip_done()
                if not payslip.nomina_cfdi:
                    payslip.action_cfdi_nomina_generate()
                cr.execute('RELEASE SAVEPOINT model_payslip_confirm_cfdi_save')
            except Exception as e:
                cr.execute('ROLLBACK TO SAVEPOINT model_payslip_confirm_cfdi_save')
                pass
        return

class OtrasEntradas(models.Model):
    _name = 'otras.entradas'

    form_id = fields.Many2one('hr.payslip.run', required=True) 
    monto = fields.Float('Monto') 
    descripcion = fields.Char('Descripcion') 
    codigo = fields.Char('Codigo')