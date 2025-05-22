from odoo import api, fields, models, tools
from odoo.exceptions import ValidationError


class ProductManufacture(models.Model):
    _name = "product.manufacture"
    _description = "Product Manufacture"

    name = fields.Char(string="Name",required=True,index=True)

    private_street = fields.Char(string="Private Street")
    building = fields.Char(string="Building")
    floor = fields.Integer(string="Floor/Room#")
    private_street2 = fields.Char(string="Private Street2")
    private_city = fields.Char(string="City")
    private_state_id = fields.Many2one("res.country.state", string="State",
        domain="[('country_id', '=?', private_country_id)]")
    private_zip = fields.Char(string="Zip")
    private_country_id = fields.Many2one("res.country", string="Country")
    phone_code = fields.Many2one('res.country.phone_code',string="Phone Code", default=lambda self: self.env.res.country.phone_code)
    private_phone = fields.Char(string="Private Phone",limit=10)
    private_email = fields.Char(string="Private Email")

    vendors = fields.Many2many('res.partner', 'product_model_vendors', 'name', 'partner_id', string='Vendors')
    phone = fields.Char(string="Phone",related="vendors.phone", store=True, readonly=False)
    email = fields.Char(string="Email",related="vendors.email", store=True, readonly=False)
    product = fields.Many2one('product.template', string='Product')

    @api.constrains('private_email')
    def _check_email_id(self):
        for rec in self:
            if not rec.private_email.endswith(".com" or ".in"):
                raise ValidationError("Email ")

