# -*- coding: utf-8 -*-

from odoo import api, models
from odoo.exceptions import UserError
#from odoo.addons.hr_payroll.wizard.hr_payroll_payslips_by_employees import HrPayslipEmployees
from datetime import datetime

class HrPayslipEmployeesExt(models.TransientModel):
    _inherit = 'hr.payslip.employees'
    

#HrPayslipEmployees.compute_sheet = HrPayslipEmployeesExt.compute_sheet
