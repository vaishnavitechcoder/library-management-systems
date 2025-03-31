from odoo import api, fields, models
from datetime import date, datetime

class LibraryAuthor(models.Model):
    _name = 'library.author'
    _description = 'Library Author'
    _order = 'name'

    seq = fields.Char()
    name = fields.Char(string="Author Name")
    biography = fields.Text(string="Biography")
    date_of_birth = fields.Datetime(string="Date of Birth")
    date_of_death = fields.Datetime(string="Date of Death")
    nationality = fields.Char(string="Nationality")
    images = fields.Image(string="Image")
    book = fields.One2many("library.books","authors_id",string="books")
    active = fields.Boolean(string="Active", default=True)
    #city_id = fields.Many2one("res.city", string="City", required=True)
    country = fields.Many2one("res.country",string="Country")
    state = fields.Many2one('res.country.state',string='States')

    def create(self, vals):
        vals['seq'] = self.env['ir.sequence'].next_by_code('library.publisher')
        return super(LibraryAuthor, self).create(vals)




