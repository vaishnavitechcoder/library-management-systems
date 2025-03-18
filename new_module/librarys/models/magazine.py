from odoo import api, fields, models
from datetime import date, datetime

class LibraryMagzine(models.Model):
    _name = "library.magazine"
    _inherit = "common.field"
    _description = "library magazine"

    freuency = fields.Selection([("weekly","Weekly"),("monthly","Monthly"),("yearly","yearly")])
