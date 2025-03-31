from odoo import api, fields, models, _
from datetime import date, datetime
from odoo.exceptions import UserError

class LibraryBorrow(models.Model):
    _name = "library.borrow"
    _description = "library borrow"
    _order = 'borrow_date desc'
    _rec_name = 'members_id'

    #borrow_id = fields.Char(string="borrow id")
    members_id = fields.Many2one('library.members',string="members",required=True)
    book_id = fields.Many2one("library.books",string="Book",required=True)
    magazine = fields.Many2one("library.magazine",string="magazine")
    borrow_date = fields.Datetime(string="Borrow Date",required=True)
    return_date = fields.Datetime(string="Return_Date")
    actual_return_date = fields.Datetime(string="Actual Return Date", readonly=True)
    fine_amount = fields.Float(string="fine amount",compute="_compute_fine_amount", store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('borrowed', 'Borrowed'),
        ('returned', 'Returned'),
        ('Late', 'Late'),
        ('Lost', 'Lost'),
    ])
    overdue_date = fields.Datetime('Due Date')
    priority = fields.Selection([('0', 'Very Low'), ('1', 'Low'), ('2', 'Normal'), ('3', 'High')], string='Priority')

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

    @ api.model
    def overdue_reminder(self):
        overdue_books = self.search([('state', '=', 'Late')])
        for book in overdue_books:
            template = self.env.ref('your_module.email_template_overdue')
            self.env['mail.template'].browse(template.id).send_mail(book.id)

    def return_book(self):
        for borrow in self:
            if borrow.state == 'Borrowed':
                if borrow.overdue_date < fields.Datetime.now():
                    borrow.state = 'Late'
                    raise UserError(_("This book is overdue! Please return it immediately."))
                borrow.state = 'Returned'
            else:
                raise UserError(_("This book has already been returned."))

    def create(self, vals):
        res = super(LibraryBorrow, self).create(vals)
        existing_borrow = self.env['library.borrow'].search([
            ('members_id', '=', res.members_id.id),
            ('book_id', '=', res.book_id.id),
            ('magazine', '=', res.magazine.id),
            ('state','=','Borrowed')
        ])
        if existing_borrow:
            raise UserError(_("You have already borrowed this book and have not returned it yet."))

        if res.book_id:
            borrowed_count = self.env['library.borrow'].search_count([
                ('book_id', '=', res.book_id.id),
                ('state', '=', 'Borrowed')
            ])

            if borrowed_count >= res.book_id.quantity:
                raise UserError(_("Sorry, this book is not available for borrowing as all copies are currently borrowed."))

        if res.magazine:
            borrowed_count = self.env['library.borrow'].search_count([
                ('magazine', '=', res.magazine.id),
                ('state', '=', 'Borrowed')
            ])

            if borrowed_count >= res.magazine.quantity:
                raise UserError(
                    _("Sorry, this magazine is not available for borrowing as all copies are currently borrowed."))

        return res