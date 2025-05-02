from odoo import models, fields, api

class InventoryStock(models.TransientModel):
    _name = 'inventory.stock'
    _inherit = 'stock.quant'


    threshold = fields.Integer(string="threshold")

    # < menuitem
    # id = "stock.menu_warehouse_report"
    # name = "Reporting"
    # sequence = "99"
    # parent = "stock.menu_stock_root"
    # groups = "group_stock_manager" / >

    @api.constrains('quantity')
    def quantity_threshold(self):
       for rec in self:
           if rec.quantity < threshold:
               return rec.product_id




