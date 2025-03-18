from odoo import models, fields
from datetime import date, datetime

class CommonField(models.AbstractModel):
    _name = "common.field"
    _description = "common field"

    name = fields.Char(string="Title",required=True)
    isbn = fields.Char(string="ISBN")
    publish_date = fields.Datetime(string="publish date",required=True)
    price = fields.Float(string="price",required=True)
    copies_available = fields.Integer(string="available copies")