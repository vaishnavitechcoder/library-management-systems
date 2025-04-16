# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class BookReport(models.Model):
    _name = "book.report"
    _description = "Books Analysis Report"

    name = fields.Char(string="Book name")
    amount_total = fields.Float(string="Amount")
    borrowed_counts = fields.Integer(string="Borrowed Copies")