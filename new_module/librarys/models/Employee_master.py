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


class salecustom(models.Model):
    _inherit = 'sale.order'

    def _delivery_count(self):
      a = super().action_confirm()
      res = self.env['stock.quant'].inventory_quantity_auto_apply
      for order in self:
          if order.delivery_count == 'True' and res.inventory_quantity_auto_apply < 5:
              raise validationError("less")
      # rec = self.env['sale.order'].delivery_count,
      return a


class AccountMove(models.Model):
     _inherit = 'account.move'

     def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('account.move')
        return super(AccountMove, self).create(vals)
