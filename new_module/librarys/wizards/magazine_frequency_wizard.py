from odoo import models, fields, api
from datetime import date, datetime


class MagazineFrequencyWizard(models.TransientModel):
    _name = 'magazine.frequency.wizard'
    _description = 'magazine frequency wizard'

    magazine_id = fields.Many2one("library.magazine", string="magazine")
    freuency = fields.Selection([
        ('weekly', 'Weekly'),
        ('yearly', 'Yearly'),
        ('monthly', 'Monthly')
    ], string="New Frequency", required=True)

    def update_active_id(self):
        active_ids = self.env.context.get('active_ids', [])
        if active_ids:
            # Loop through all active IDs
            for active_id in active_ids:
                record = self.env['library.magazine'].browse(active_id)
                record.write({'freuency': self.freuency})
        return True