from odoo import models, fields, api
from datetime import date, datetime


class EmployeeWizard(models.TransientModel):
    _name = 'employee.wizard'
    _inherit = 'hr.employee'


    def get_data(self):
        for rec in self:


                 print(rec)