from odoo import models, fields
from datetime import date, datetime

class CommonField(models.AbstractModel):
    _name = "common.field"
    _description = "common field"

    name = fields.Char(string="Title",required=True)
    isbn = fields.Char(string="ISBN")
    publish_date = fields.Datetime(string="publish date",required=True)
    locations = fields.Many2one("stock.location",string="location")
    currency_id = fields.Many2one('res.currency', string='Currency',default=lambda self: self.env.company.currency_id)
    amount_total = fields.Monetary(string='Total', currency_field='currency_id')
    #copies_available = fields.Integer(string="available copies")
