from odoo import api, fields, models
from datetime import date, datetime

class LibraryMembers(models.Model):
    _name = "library.members"
    _description = "library members"
    _rec_name = 'name'
    _order = 'name asc'

    members_id = fields.Char(string="member id",required=True)
    name = fields.Char(string="name",required=True)
    email = fields.Char(string="email",required=True)
    phone_num = fields.Char(string="phone number")
    address = fields.Char(string="address")
    joining_date = fields.Datetime(string="joining date",default=fields.Date.context_today)
    status = fields.Selection([('activate','Activate'),('deactivate','Deactivate')],string='status')
