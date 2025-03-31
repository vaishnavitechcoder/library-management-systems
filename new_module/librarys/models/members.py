from odoo import api, fields, models
from datetime import date, datetime

class LibraryMembers(models.Model):
    _name = "library.members"
    _description = "library members"
    _rec_name = 'names'
    _order = 'names asc'

    seq = fields.Char()
    names = fields.Char(string="name",required=True)
    email = fields.Char(string="email",required=True)
    phone_num = fields.Char(string="phone number")
    address = fields.Char(string="address")
    #city_id = fields.Many2one("res.city", string="City", required=True)
    country = fields.Many2one("res.country",string="Country")
    state = fields.Many2one('res.country.state',string='States')
    joining_date = fields.Datetime(string="joining date",default=fields.Date.context_today)
    status = fields.Selection([('activate','Activate'),('deactivate','Deactivate')],string='status')

    def create(self, vals):
        vals['seq'] = self.env['ir.sequence'].next_by_code('library.publisher')
        return super(LibraryMembers, self).create(vals)
