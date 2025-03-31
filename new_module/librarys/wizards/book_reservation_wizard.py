from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date, datetime

class BookReservationWizard(models.TransientModel):
    _name = 'library.book.reservation.wizard'
    _description = 'library Book Reservation Wizard'

    books_id = fields.Many2one('library.books', string='Book', required=True)
    member_id = fields.Many2one('library.members', string='Member', required=True)
    reservation_date = fields.Datetime(string='Reservation Date', default=fields.Date.today)
    status = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')], string='Status')


    @api.constrains('book_id')
    def _check_book_availability(self):
        for record in self:
            if record.books_id.available_copies <= 0:
                raise ValidationError('No copies available for reservation!')

    def action_confirm(self):
        for record in self:
            if record.books_id.available_copies > 0:
                record.books_id.available_copies -= 1
                record.status = 'confirmed'

                # Create a permanent reservation record in the main model
                self.env['library.reservation'].create({
                    'books_id': record.books_id.id,
                    'member_id': record.member_id.id,
                    'reservation_date': record.reservation_date,
                    'status': 'confirmed'
                })
            else:
                raise ValidationError('No available copies!')
                
    def action_cancel(self):
        for record in self:
            record.status = 'cancelled'