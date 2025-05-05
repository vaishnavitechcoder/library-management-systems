# models/low_stock_wizard.py
from odoo import models, fields, api

class LowStockReportWizard(models.TransientModel):
    _name = 'low.stock.report.wizard'
    _description = 'Low Stock Report Wizard'

    threshold_qty = fields.Float(string="Threshold Quantity", required=True)

    def action_generate_report(self):
        products = self.env['product.product'].search([('qty_available', '<', self.threshold_qty)])
        return {
            'name': 'Low Stock Products',
            'type': 'ir.actions.act_window',
            'res_model': 'product.product',
            'view_mode': 'list,form',
            'domain': [('id', 'in', products.ids)],
            'target': 'current',
        }


