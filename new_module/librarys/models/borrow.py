from odoo import api, fields, models
from datetime import date, datetime

class LibraryBorrow(models.Model):
    _name = "library.borrow"
    _description = "library borrow"
    _order = 'borrow_date desc'

    borrow_id = fields.Char(string="borrow id", copy=False, index=True)
    members_id = fields.Many2one('library.members',string="member id",required=True)
    book_id = fields.Many2one("library.books",string="Book",required=True)
    borrow_date = fields.Datetime(string="Borrow Date",required=True)
    return_date = fields.Datetime(string="Return_Date")
    actual_return_date = fields.Datetime(string="Actual Return Date", readonly=True)
    fine_amount = fields.Float(string="fine amount",compute="_compute_fine_amount", store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('borrowed', 'Borrowed'),
        ('returned', 'Returned')], default='borrowed')

    """@api.depends('return_date')
    def _compute_fine_amount(self):
        fine_per_day = 5.0
        for record in self:
            if record.return_date and record.return_date < fields.Datetime.context_today(self) and record.state != 'returned':
                days_overdue = (fields.Datetime.context_today(self) - record.return_date).days
                record.fine_amount = days_overdue * fine_per_day
            else:
                record.fine_amount = 0.0"""
    

    @api.depends('return_date', 'actual_return_date')
    def _compute_fine_amount(self):
        fine_per_day = 5.0
        for record in self:
            if record.return_date and record.actual_return_date:
                if record.actual_return_date > record.return_date:
                    days_overdue = (record.actual_return_date - record.return_date).days
                    record.fine_amount = days_overdue * fine_per_day
                else:
                    record.fine_amount = 0.0
            else:
                record.fine_amount = 0.0

    def action_borrow(self):
        for record in self:
            record.state = 'borrowed'

    def action_return(self):
        for record in self:
            record.actual_return_date = fields.Datetime.now()
            record.state = 'returned'
            record._compute_fine_amount()
            return {
                'effect': {
                    'fadeout': 'slow',
                    'message': 'Book returned successfully!',
                    'type': 'rainbow_man',
                }
            }

    def action_cancel(self):
        for record in self:
            record.state = 'draft'
            record.actual_return_date = False
            record.fine_amount = 0.0
