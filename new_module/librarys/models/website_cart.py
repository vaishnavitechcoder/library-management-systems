from odoo import models, fields


class LibraryCart(models.Model):
    _name = 'library.cart'
    _description = 'Library Cart'

    user_id = fields.Many2one('res.users', string='User', required=True)
    book_id = fields.Many2one('library.books', string='Book', required=True)
    quantity = fields.Integer(string='Quantity', default=1)
