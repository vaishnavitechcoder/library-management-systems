
from odoo import fields, models


class Library_Management_System(models.TransientModel):
    _inherit = 'res.config.settings'

    email_reminder = fields.Boolean(string="Enable Email Reminders")