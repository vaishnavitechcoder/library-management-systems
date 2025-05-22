from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    seq = fields.Char()

    @api.constrains('work_email')
    def _check_email_id(self):
        for rec in self:
            if not rec.work_email.endswith("@yourcompany.com"):
                raise ValidationError("ends with @ yourcompany.com")

    def create(self, vals):
        vals['seq'] = self.env['ir.sequence'].next_by_code('hr.employee')
        return super(HrEmployee, self).create(vals)


from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        for picking in self:
            if picking.picking_type_id.code == 'outgoing':
                for move in picking.move_ids_without_package:
                    product = move.product_id
                    qty_available = product.qty_available
                    if qty_available < 5:
                        raise UserError(_(
                            "Product '%s' has only %.2f in stock. "
                            "Minimum required is 5 units." % (product.display_name, qty_available)
                        ))
        return super().button_validate()


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('ref'):
                vals['ref'] = self.env['ir.sequence'].next_by_code('account.move')

        return super(AccountMove, self).create(vals_list)


class StockPickingCustom(models.Model):
    _inherit = 'stock.picking'

    total_weight = fields.Integer(string="total weight", compute="_compute_total_weight")

    @api.depends('move_ids.product_id', 'move_ids.product_uom_qty')
    def _compute_total_weight(self):
        for picking in self:
            total = 0.0
            for move in picking.move_ids:
                product_weight = move.product_id.weight or 0.0
                total += product_weight * move.product_uom_qty
            picking.total_weight = total


class AccountMoveAuditor(models.Model):
    _inherit = 'account.move'

    auditor_approval = fields.Boolean(string="Auditor approval", default=True)


from datetime import datetime, timedelta


class HrEmployeeSalary(models.Model):
    _inherit = 'hr.contract'

    @api.depends('employee_id.wage', 'employee_id.contract_wage')
    def _employee_minimum_wage(self):
        for rec in self:
            if rec.wage < rec.contact_wage:
                raise ValidationError(_("employee wage is less than contract wage"))

    # # HR Email - you can hardcode or fetch from config/settings
    # hr_email = 'hr@example.com'
    #
    # @api.model
    # def remainder_email(self):
    #     contracts = self.search([('date_end', '=', 'date_end')])
    #     template = self.env.ref('librarys.contract_end_reminder_email_template')
    #     hr_email = 'hr@example.com'
    #
    #     for contract in contracts:
    #         if template:
    #             template.send_mail(contract.id, force_send=True, email_values={
    #                 'email_to': hr_email
    #             })


class OrderCustom(models.Model):
    _inherit = 'sale.order'

    DEFAULT_SEPARATOR = '-'

    @api.depends('validity_date', 'date_order')
    def expiration_date(self):
        for rec in self:
            validate = rec.validate_date.Datetime.timedelta(days=5) > date_order
            return validate

    def _restrict_user(self):
        for rec in self:
            if rec.date_order != Datetime.now().timestamp():
                raise validationError(_("date order is backdate"))

    def add_default_sep(self):
        if client_order_ref in self:
            s = ""
            n = ""
            for c in client_order_ref:
                if c.isdigit():
                    n += c
                else:
                    s += c
            return '-'.join(s, n)


# options="{'no_create': True, 'no_open': True}


class ProductTemplateCustom(models.Model):
    _inherit = 'product.template'

    authorized_manufacture_id = fields.Many2one('product.manufacture', string='Authorised Manufacture')
