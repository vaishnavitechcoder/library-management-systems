# Import necessary libraries for email processing
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class MailMail(models.Model):
    _inherit = 'mail.mail'

    @api.model
    def process_incoming_emails(self):
        # Fetch and process incoming emails
        incoming_emails = self.search([('state', '=', 'incoming')])
        for email in incoming_emails:
            try:
                # Process each incoming email
                email.process_incoming_emails()
            except Exception as e:
                _logger.error(f"Error processing email {email.id}: {str(e)}")
