from odoo import api, fields, models, _
from datetime import date, datetime

SALE_ORDER_STATE = [
    ('draft', "Quotation"),
    ('sent', "Quotation Sent"),
    ('sale', "Sales Order"),
    ('cancel', "Cancelled"),
]


class LibraryPublisher(models.Model):
    _name = "library.publisher"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "library publisher"
    _rec_name = "name"

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
    state = fields.Selection(
        selection=SALE_ORDER_STATE,
        string="Status",
        readonly=True, copy=False, index=True,
        tracking=3,
        default='draft')

    order_line = fields.One2many(
        comodel_name='sale.order.line',
        inverse_name='order_id',
        string="Order Lines",
        copy=True, auto_join=True)

    type_name = fields.Char(string="Type Name", compute='_compute_type_name')

    def create(self, vals):
        vals['seq'] = self.env['ir.sequence'].next_by_code('library.publisher')
        return super(LibraryPublisher, self).create(vals)

    #def action_send_email(self):
        #template = self.env.ref('librarys.mail_template_publishers')
        #for rec in self:
            #template.send_mail(rec.id, force_send=True)

    def action_quotation_send(self):
        """ Opens a wizard to compose an email, with relevant mail template loaded by default """
        self.filtered(lambda so: so.state in ('draft', 'sent')).order_line._validate_analytic_distribution()
        lang = self.env.context.get('lang')

        ctx = {
             'default_model': 'library.publisher',
            'default_res_ids': self.ids,
            'default_composition_mode': 'comment',
            'proforma': self.env.context.get('proforma', False),
        }

        if len(self) > 1:
            ctx['default_composition_mode'] = 'mass_mail'
        else:
            ctx.update({
                'force_email': True,
                'model_description': self.with_context(lang=lang).type_name,
            })
            if not self.env.context.get('hide_default_template'):
                mail_template = self.env.ref('librarys.mail_template_publishers', raise_if_not_found=False)
                if mail_template:
                    ctx.update({
                        'default_template_id': mail_template.id,
                        'mark_so_as_sent': True,
                    })
                if mail_template and mail_template.lang:
                    lang = mail_template._render_lang(self.ids)[self.id]
            else:
                for order in self:
                    order._portal_ensure_token()

        action = {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }
        if (
                self.env.context.get('check_document_layout')
                and not self.env.context.get('discard_logo_check')
                and self.env.is_admin()
                and not self.env.company.external_report_layout_id
        ):
            layout_action = self.env['ir.actions.report']._action_configure_external_report_layout(
                action,
            )
            # Need to remove this context for windows action
            action.pop('close_on_report_download', None)
            layout_action['context']['dialog_size'] = 'extra-large'
            return layout_action
        return action

    def _find_mail_template(self):
        """ Get the appropriate mail template for the current sales order based on its state.

        If the SO is confirmed, we return the mail template for the sale confirmation.
        Otherwise, we return the quotation email template.

        :return: The correct mail template based on the current status
        :rtype: record of `mail.template` or `None` if not found
        """
        self.ensure_one()
        if self.env.context.get('proforma') or self.state != 'sale':
            return self.env.ref('librarys.mail_template_publishers', raise_if_not_found=False)
        else:
            return self._get_confirmation_template()

    @api.depends('state')
    def _compute_type_name(self):
        for record in self:
            if record.state in ('draft', 'sent', 'cancel'):
                record.type_name = _("Quotation")
            else:
                record.type_name = _("Sales Order")


    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        args = list(args or [])
        if name :
            args += ['|', '|' ,
                     ('name', operator, name),
                     ('email', operator, name),
                     ('phone', operator, name)]
            return self._search(args, limit=limit, access_rights_uid=name_get_uid)

    def action_trigger(self):
        # This is the function that will be triggered by the button.
        for partner in self:
            partner.write({'is_company': True})  # Example action: set 'is_company' to True
        return True