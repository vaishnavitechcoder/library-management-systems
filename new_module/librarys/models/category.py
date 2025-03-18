from odoo import api, fields, models
from datetime import date, datetime

class LibraryCategory(models.Model):
    _name = "library.category"
    _description = "library category"
    _rec_name = 'name'
    _order = 'name asc'

    name = fields.Char(string="category_name",required=True)
    code = fields.Char(string="code",required=True)
    languages = fields.Selection([('english', 'English'),
                                 ('french', 'French'),
                                 ('spanish', 'Spanish'),
                                 ('german', 'German'),
                                 ('other', 'Other')],
    string="languages",default="english")
    sub_type = fields.Char(string="sub type")

