from odoo import api, fields, models
from datetime import date, datetime


class LibraryPublisher(models.Model):
    _name = "library.publisher"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "library publisher"

    seq = fields.Char()
    name = fields.Many2one("res.partner", string="Publisher", change_default=True, index=True)
    function = fields.Char(string='Job Position', related="name.function", store=True, readonly=False)
    phone = fields.Char(string="phone", related="name.phone", store=True, readonly=False)
    mobile = fields.Char(string="mobile", related="name.mobile", store=True, readonly=False)
    email = fields.Char(string="email", related="name.email", store=True, readonly=False)
    website = fields.Char(string="website", related="name.website", store=True, readonly=False)

    founded = fields.Date(string="Founded", store=True, readonly=False)
    books = fields.One2many("library.books", "publisher", string="Books")
    image = fields.Image(string="Image")
    priority = fields.Selection([('0', 'Very Low'), ('1', 'Low'), ('2', 'Normal'), ('3', 'High')], string='Priority')

    def create(self, vals):
        vals['seq'] = self.env['ir.sequence'].next_by_code('library.publisher')
        return super(LibraryPublisher, self).create(vals)


    def action_send_email(self):
        template = self.env.ref('librarys.mail_template_publishers')
        for rec in self:
            template.send_mail(rec.id, force_send=True)

