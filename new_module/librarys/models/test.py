from odoo import api, fields, models
from odoo.exceptions import ValidationError


class VendorCustom(models.Model):
    _name = "vendor.master"
    _description = "Vendor Master"

    # name = fields.Many2one('product.manufacture', string="Name")
    # vendors = fields.Many2many('res.partner', 'product_model_vendors', 'name', 'partner_id', string='Vendors')
    # phone = fields.Char(string="Phone",related="vendors.phone", store=True, readonly=False)
    # email = fields.Char(string="Email",related="vendors.email", store=True, readonly=False)