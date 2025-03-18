from odoo import api, fields, models
from datetime import date, datetime

class LibraryFines(models.Model):
    _name = "library.fines"
    _description = "library fines"
    _order = 'fine_date desc'

    member_id = fields.Many2one("library.members",string="member id",required=True)
    borrow_id = fields.Many2one("library.borrow",string="borrow id",required=True)
    book_id = fields.Many2one("library.books",string="book id",required=True)
    fine_type = fields.Selection([("late return","Late Return"),
                                  ("lost book","Lost Book"),
                                  ("damage","Damage")],string="fine type")
    amount = fields.Float(string="amount",required=True)
    fine_date = fields.Datetime(string="fine date")
    due_date = fields.Datetime(string="due date")
    status = fields.Selection([("paid","Paid"),("pending","Pending"),
                                ("over due","Over Due")],string="status",default="pending")
    payment_date = fields.Datetime(string="payment date")
    payment_method = fields.Selection([("cash","Cash"),
                                  ("online","Online"),
                                  ("card","Card")],string="payment method")