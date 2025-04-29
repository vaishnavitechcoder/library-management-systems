from odoo import api, fields, models
from datetime import date, datetime

class LibraryFines(models.Model):
    _name = "library.fines"
    _description = "library fines"
    _order = 'fine_date desc'
    _rec_name = 'member_id'

    member_id = fields.Many2one("library.borrow",string="member id",required=True)
    book_id = fields.Many2one(related="member_id.book_id",store=True,readonly=True,string="book id")
    fine_amount = fields.Float(string="fine amount", related="member_id.fine_amount",readonly=True, store=True)
    fine_type = fields.Selection(related="member_id.state", store=True, readonly=True,string="fine type")
    fine_date = fields.Date(string="fine date")
    due_date = fields.Date(related="member_id.actual_return_date",store=True, readonly=True, string="due date")
    status = fields.Selection([("paid","Paid"),("pending","Pending"),
                                ("over due","Over Due")],string="status",default="pending")
    payment_date = fields.Datetime(string="payment date")
    payment_method = fields.Selection([("cash","Cash"),
                                  ("online","Online"),
                                  ("card","Card")],string="payment method")
    priority = fields.Selection([('0', 'Very Low'), ('1', 'Low'), ('2', 'Normal'), ('3', 'High')], string='Priority')
    note = fields.Html(string='Description on the Payment', translate=True)