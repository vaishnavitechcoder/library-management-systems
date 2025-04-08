from odoo import api, fields, models, _
from datetime import date, datetime
from odoo.exceptions import ValidationError

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

    @api.model
    def test_cron_job(self):
            print("abcd")

    @api.autovacuum
    def _autovaccum_records(self):
        inactive_members = self.env['library.members'].search([('status', '=', 'deactivate')])
        inactive_members.unlink()

    def action_notification(self):
        message: "button click sucessfully"
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _("Operation Successful"),
                'type': 'success',
                'message': "button click sucessfully",
                'sticky': False,
            },
        }

    def get_data(self):
        print("get_data_method")
        members = self.env["library.members"].search([])
        for rec in members:
            print(rec)


    def action_share_whatsapp(self):
        if not self.phone_num:
            raise ValidationError(_("missing phone number in members record"))
        msg = "HI %s" % self.names
        whatsapp_api_url = "https://api.whatsapp.com/send?phone=%s&text=%s" % (self.phone_num, msg)
        return {
            "type": "ir.actions.act_url",
            "url": whatsapp_api_url,
            "target": "new"
        }

