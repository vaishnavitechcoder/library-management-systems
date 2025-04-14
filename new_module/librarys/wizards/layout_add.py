
from odoo import models, fields


class View(models.Model):
    _inherit = 'report.layout'

    type = fields.Selection([
        ('modern', 'Modern')
    ])


