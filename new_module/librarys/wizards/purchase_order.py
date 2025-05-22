from odoo import models, fields, api
from odoo.exceptions import UserError
import io
import base64
import xlsxwriter


class PurchaseOrderWizard(models.TransientModel):
    _name = 'purchase.order.wizard'
    _description = 'Purchase Wizard to export selected employees to Excel'

    vendors = fields.Many2many('res.partner', string="Vendors")
    file_name = fields.Char(string="File Name", default="employee_export.xlsx")
    file_data = fields.Binary(string="Download Excel", readonly=True)

    def export_vendor(self):

        if not self.vendors:
            raise UserError("No vendors selected.")

            # Filter Purchase Orders by selected vendors
        purchase_orders = self.env['purchase.order'].search([('partner_id', 'in', self.vendors.ids)])
        if not purchase_orders:
            raise UserError("No Purchase Orders found for selected vendors.")

        # Create the Excel file
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet("Vendors")

        headers = ['PO#', 'Date', 'Vendor Name', 'PO Status', 'Total Amount']
        for col, header in enumerate(headers):
            sheet.write(0, col, header)

        for row, po in enumerate(purchase_orders, start=1):
            sheet.write(row, 0, po.name or '')
            sheet.write(row, 1, str(po.date_order or ''))
            sheet.write(row, 2, po.partner_id.name or '')
            sheet.write(row, 3, po.state or '')
            sheet.write(row, 4, float(po.amount_total or 0.0))

        workbook.close()
        output.seek(0)

        self.file_data = base64.b64encode(output.read())
        self.file_name = "vendors_export.xlsx"

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'purchase.order.wizard',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
        }

    def send_with_attachment(self):
        attachment = self.env['ir.attachment'].create({
            'name': 'vendors_export.xlsx',
            'type': 'binary',
            'mimetype': 'xlsx',
            'datas': self.file_data,
        })
        return attachment
