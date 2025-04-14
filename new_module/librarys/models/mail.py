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


    def send_report_with_attachment(self):
            # Define the email template
        email_template = self.env.ref('librarys.mail_template_publishers')

            # Prepare the email with the PDF attached
        attachment = self.env['ir.attachment'].create({
                'name': 'Report.pdf',
                'type': 'binary',
                'mimetype': 'application/pdf',
            })

            # Attach the generated PDF to the email
        email_template.attachment_ids = [(4, attachment.id)]

            # Send the email
        email_template.send_mail(self.id, force_send=True)