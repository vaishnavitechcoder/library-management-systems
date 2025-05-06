from odoo import models, fields, api
from odoo.exceptions import UserError
import io
import base64
import xlsxwriter


class VendorSelected(models.TransientModel):
    _name = 'vendor.selected'
    _description = 'vendor selected'

    # vendors = fields.Many2many('res.partner', 'vendor_purchase_wizard' , string='Vendors',
    #                           context={'res_partner_search_mode': 'supplier'})

    vendors = fields.Many2many('product.supplierinfo', 'vendor_purchase_wizard_supper', string='Vendors')


    def check_vendor(self):
        vendors = self.env['purchase.order'].search([('state', '=', 'purchase')])
        return {
              'name': 'Selected Vendors',
              'type': 'ir.actions.act_window',
              'res_model': 'purchase.order',
              'view_mode': 'list,form',
              'domain': [('id', 'in', vendors.ids)],
              'target': 'current',
              'context':"{'res_partner_search_mode': 'supplier'}"
            }
