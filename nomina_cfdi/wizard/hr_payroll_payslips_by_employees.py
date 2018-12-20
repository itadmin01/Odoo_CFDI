# -*- coding: utf-8 -*-

from odoo import api, models


class HrPayslipEmployees(models.TransientModel):
    _inherit = 'hr.payslip.employees'

    @api.multi
    def compute_sheet(self):
        res = super(HrPayslipEmployees, self).compute_sheet()
        active_id = self.env.context.get('active_id')
        if active_id and self.employee_ids:
            payslips = self.env['hr.payslip'].search([('employee_id', '=', self.employee_ids.ids), ('payslip_run_id', '=', active_id)])
            payslip_batch = self.env['hr.payslip.run'].browse(active_id)
            payslips.write({'tipo_nomina': payslip_batch.tipo_nomina})
        return res
    
        
