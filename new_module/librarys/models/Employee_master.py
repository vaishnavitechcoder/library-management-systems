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

     # def create(self, vals):
     #    vals['ref'] = self.env['ir.sequence'].next_by_code('account.move')
     #    return super(AccountMove, self).create(vals)

     @api.model
     def create(self, vals_list):
         if isinstance(vals_list, dict):
             vals_list = [vals_list]

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

    auditor_approval = fields.Boolean(string="Auditor approval",default=True)


class HrEmployeeSalary(models.Model):
    _inherit = 'hr.contract'

    @api.depends('employee_id.wage', 'employee_id.contract_wage')
    def _employee_minimum_wage(self):
        for rec in self:
            if rec.wage < rec.contact_wage:
                raise ValidationError(_("employee wage is less than contract wage"))






