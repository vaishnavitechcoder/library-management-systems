
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    email_reminder = fields.Boolean(string="Enable Email Reminders")