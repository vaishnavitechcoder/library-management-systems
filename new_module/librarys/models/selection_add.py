
from odoo import models, fields


class LibraryCategory(models.Model):
    _inherit = 'library.category'

    languages = fields.Selection(selection_add=[
        ('marathi', 'Marathi'),
        ('hindi', 'Hindi'),
        ('gujarati', 'Gujarati')
    ], string="Languages", default='marathi')


   #https://useopenerp.com/v8/model/mail-message#
