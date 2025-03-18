from odoo import api, fields, models
from datetime import date, datetime

class LibraryAuthor(models.Model):
    _name = 'library.author'
    _description = 'Library Author'
    _order = 'name'

    name = fields.Char(string="Author Name", required=True)
    biography = fields.Text(string="Biography")
    date_of_birth = fields.Datetime(string="Date of Birth")
    date_of_death = fields.Datetime(string="Date of Death")
    nationality = fields.Char(string="Nationality")
    images = fields.Image(string="Image")
    book_ids = fields.Many2many('library.books', 'library_book_author_rel', 'author_id', 'book_id', string="Books")
    active = fields.Boolean(string="Active", default=True)
