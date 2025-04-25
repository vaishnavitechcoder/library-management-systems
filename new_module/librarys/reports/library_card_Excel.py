from odoo import models

class MembersXlsx(models.AbstractModel):
    _name = 'report.librarys.report_library_card_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    _description = "Excel report"

    def generate_xlsx_report(self, workbook, data, objects):
        sheet = workbook.add_worksheet("Library Cards")
        bold = workbook.add_format({'bold': True})

        # Header
        sheet.write(0, 0, 'Name', bold)
        sheet.write(0, 1, 'Email', bold)
        sheet.write(0, 2, 'Phone Number', bold)
        sheet.write(0, 3, 'Address', bold)
        sheet.write(0, 4, 'Country', bold)
        sheet.write(0, 5, 'State', bold)
        sheet.write(0, 6, 'Joining Date', bold)
        sheet.write(0, 7, 'Status', bold)

        row = 1
        for obj in objects:
            sheet.write(row, 0, obj.names or '')
            sheet.write(row, 1, obj.email or '')
            sheet.write(row, 2, obj.phone_num or '')
            sheet.write(row, 3, obj.address or '')
            sheet.write(row, 4, obj.country.name if obj.country else '')
            sheet.write(row, 5, obj.state.name if obj.state else '')
            sheet.write(row, 6, str(obj.joining_date or ''))
            sheet.write(row, 7, obj.status or '')
            row += 1