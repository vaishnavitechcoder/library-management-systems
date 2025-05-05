from odoo import models, fields, api
from odoo.exceptions import UserError
import io
import base64
import xlsxwriter


class EmployeeExportWizard(models.TransientModel):
    _name = 'employee.export.wizard'
    _description = 'Wizard to export selected employees to Excel'

    file_name = fields.Char(string="File Name", default="employee_export.xlsx")
    file_data = fields.Binary(string="Download Excel", readonly=True)

    def export_employees(self):
        active_ids = self.env.context.get('active_ids')
        if not active_ids:
            raise UserError("No employees selected.")

        employees = self.env['hr.employee'].browse(active_ids)

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet("Employees")

        headers = ['Name', 'Work Email', 'Job Title', 'Department']
        for col, header in enumerate(headers):
            sheet.write(0, col, header)

        for row, employee in enumerate(employees, start=1):
            sheet.write(row, 0, employee.name or '')
            sheet.write(row, 1, employee.work_email or '')
            sheet.write(row, 2, employee.job_title or '')
            sheet.write(row, 3, employee.department_id.name or '')

        workbook.close()
        output.seek(0)

        self.file_data = base64.b64encode(output.read())
        self.file_name = "employees_export.xlsx"

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'employee.export.wizard',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
        }
