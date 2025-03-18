from odoo import models, fields, api
from datetime import date, datetime

class BookReservation(models.Model):
    _name = 'library.reservation'
    _description = 'library Reservation'

    book_id = fields.Many2one('library.books', string='Book', required=True)
    member_id = fields.Many2one('library.members', string='Member', required=True)
    reservation_date = fields.Datetime(string='Reservation Date', default=fields.Date.today)
    status = fields.Selection(
        [('draft', 'Draft'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')],
        string='Status', default='draft'
    )
