from odoo import api, fields, models, _
from datetime import date, datetime
from odoo.exceptions import UserError


class LibraryMagzine(models.Model):
    _name = "library.magazine"
    _inherit = ['common.field','mail.thread','mail.activity.mixin']
    _description = "library magazine"

    freuency = fields.Selection([("weekly", "Weekly"), ("monthly", "Monthly"), ("yearly", "yearly")],
                                string="frequency",tracking=True)
    quantity = fields.Integer(string="quantity", required=True)
    available_copies = fields.Integer(string="available_copies", compute="_compute_available_copies")
    borrow_ids = fields.One2many("library.borrow", "magazine", string="borrows_ids")
    borrowed_count = fields.Integer(string="Borrowed Copies", compute="_compute_borrowed_count")

    @api.depends('quantity', 'borrow_ids.state')
    def _compute_available_copies(self):
        for record in self:
            borrowed_count = len(record.borrow_ids.filtered(lambda b: b.state == 'borrowed'))
            record.available_copies = record.quantity - borrowed_count

    @api.depends('borrow_ids.state')
    def _compute_borrowed_count(self):
        for record in self:
            # Count the borrow records that are in 'borrowed' state
            record.borrowed_count = len(record.borrow_ids.filtered(lambda b: b.state == 'borrowed'))

    @api.constrains('available_copies', 'quantity')
    def _check_available_copies(self):
        for record in self:
            if record.available_copies < 0:
                raise UserError(_("Available copies cannot be negative."))
            if record.available_copies > record.quantity:
                raise UserError(_("Available copies cannot exceed the total quantity of magazines."))

    def create(self, vals):
        vals['seq'] = self.env['ir.sequence'].next_by_code('library.publisher')
        return super(LibraryPublisher, self).create(vals)

    def action_weekly(self):
        for record in self:
            record.freuency = "weekly"

