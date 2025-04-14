
from odoo import fields, models


class Library_Management_System(models.TransientModel):
    _inherit = 'res.config.settings'

    email_reminder = fields.Boolean(string="Enable Email Reminders")

    layout_choice = fields.Selection([
        ('basic', 'Basic'),
        ('creative', 'Creative'),
        ('artistic', 'Artistic')
    ], string="Default Report Layout", config_parameter='librarys.layout_choice')

    def open_layout_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'layout.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_layout_choice': self.layout_choice,
            }
        }


