from odoo import api, fields, models
from datetime import date, datetime

class LibraryBooks(models.Model):
    _name = "library.books"
    _inherit = "common.field"
    _description = "library books"


    book_id = fields.Char(string="book id",required=True,copy=False)
    #name = fields.Char(string="Title",required=True)
    author_ids = fields.Many2many('library.author', 'library_book_author_rel', 'book_id', 'author_id', string="Authors")
    #isbn = fields.Char(string="ISBN")
    category_id = fields.Many2one("library.category", string="Book Type", required=True)
    publisher = fields.Char(string="publisher")
    #publish_date = fields.Datetime(string="publish date",required=True)
    num_pages= fields.Integer(string="Number of Pages")
    language = fields.Selection([('english', 'English'),
                                 ('french', 'French'),
                                 ('spanish', 'Spanish'),
                                 ('german', 'German'),
                                 ('other', 'Other')],
        string="languages",default="english")
    state = fields.Selection([ ('available', 'Available'),
                             ('borrowed', 'Borrowed'),
                              ('reserved', 'Reserved'),
                             ('lost', 'Lost')],
        string="state",default="available")
    #price = fields.Float(string="price",required=True)
    image = fields.Image(string="cover image")
    description = fields.Text(string="description",required=True)
    location = fields.Char(string="location")
    quantity = fields.Integer(string="quantity",default=True)
    available_copies = fields.Integer(string="available_copies",compute="_compute_available_copies")
    borrow_ids = fields.One2many("library.borrow","book_id",string="borrows_ids")
    code = fields.Many2one("library.category",string="code")
    borrowed_count = fields.Integer(string="Borrowed Copies", compute="_compute_borrowed_count")
    active = fields.Boolean(string="Active",default=True)

    @api.depends('quantity', 'borrow_ids.state')
    def _compute_available_copies(self):
            for books in self:
                borrowed_count = sum(1 for borrow in books.borrow_ids if borrow.state == 'borrowed')
                books.available_copies = books.quantity - borrowed_count
    
    @api.depends('borrow_ids.state')
    def _compute_borrowed_count(self):
        for books in self:
            books.borrowed_count = len(books.borrow_ids.filtered(lambda b: b.state == 'borrowed'))

    def action_reserve_book(self):
        return {
           'name': 'Reserve Book',
           'type': 'ir.actions.act_window',
           'res_model': 'library.book.reservation.wizard',
           'view_mode': 'form',
           'target': 'new'
    }

    @api.depends('borrow_ids')
    def _compute_borrow_count(self):
        for record in self:
            record.borrowed_count = len(record.borrow_ids)
