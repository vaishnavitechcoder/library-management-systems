from odoo import models, fields, api
from odoo.exceptions import UserError
import io
import base64
import xlsxwriter


class PurchaseOrderWizard(models.TransientModel):
    _name = 'purchase.order.wizard'
    _description = 'Purchase Wizard to export selected employees to Excel'

    file_name = fields.Char(string="File Name", default="employee_export.xlsx")
    file_data = fields.Binary(string="Download Excel", readonly=True)

    def export_vendor(self):
        active_ids = self.env.context.get('active_ids')
        if not active_ids:
            raise UserError("No Vendors selected.")

        selected_vendors = self.env['res.partner'].browse(active_ids).exists()
        if not selected_vendors:
            raise UserError("Selected vendors do not exist.")

        vendors = self.env['purchase.order'].search([('partner_id', 'in', selected_vendors.ids)])
        if not vendors:
            raise UserError("No Purchase Orders found for selected vendors.")
        # vendors = self.env['purchase.order'].browse(active_ids)

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet("Vendors")

        headers = ['PO#', 'Date', 'Vendor Name', 'PO Status', 'Total Amount']
        for col, header in enumerate(headers):
            sheet.write(0, col, header)


        for row, vendor in enumerate(vendors, start=1):
            sheet.write(row, 0, vendor.name or '')
            sheet.write(row, 1, str(vendor.date_order or ''))
            sheet.write(row, 2, vendor.partner_id.name or '')
            sheet.write(row, 3, vendor.state or '')
            sheet.write(row, 4, float(vendor.amount_total or 0.0))

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

        # Prepare the email with the PDF attached
        attachment = self.env['ir.attachment'].create({
            'name': 'vendors_export.xlsx',
            'type': 'binary',
            'mimetype': 'xlsx',
            'datas': self.file_data,
        })
        return attachment
