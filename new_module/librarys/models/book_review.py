from odoo import api, fields, models
from datetime import date, datetime


class LibraryReview(models.Model):
    _name = 'library.review'
    _description = 'Book Review'

    book_id = fields.Many2one('library.books',string="book")
    user_id = fields.Many2one('res.users',string="user")
    rating = fields.Integer()
    comment = fields.Text()
    date = fields.Datetime(default=fields.Datetime.now)
