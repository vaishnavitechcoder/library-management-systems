from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)

from markupsafe import Markup

from odoo.addons.base.models.ir_qweb_fields import nl2br
from odoo.tools import html2plaintext, is_html_empty, image as tools
from odoo.tools.misc import file_path

try:
    import sass as libsass
except ImportError:
    # If the `sass` python library isn't found, we fallback on the
    # `sassc` executable in the path.
    libsass = None
try:
    from PIL.Image import Resampling
except ImportError:
    from PIL import Image as Resampling

DEFAULT_PRIMARY = '#000000'
DEFAULT_SECONDARY = '#000000'


class LayoutWizard(models.TransientModel):
    _name = 'layout.wizard'
    _description = 'Layout Configuration Wizard'

    layout_choice = fields.Selection([
        ('basic', 'Basic'),
        ('creative', 'Creative'),
        ('artistic', 'Artistic')
    ], string="Selected Layout", required=True)

    preview = fields.Html(compute='_compute_preview', sanitize=False)

    def apply_layout(self):
        # Determine the report template to use
        if self.layout_choice == 'artistic':
            report_name = 'librarys.reports_publishers_cards'
        else:
            report_name = 'librarys.report_publisher_card'

        # Return a report action to render the QWeb report in the browser
        return {
            'type': 'ir.actions.report',
            'report_type': 'qweb-html',  # or 'qweb-pdf' if you want PDF
            'report_name': report_name,
            'report_file': report_name,
            'name': "Publisher Layout Preview",
        }


    def _get_preview_template(self):
        if self.layout_choice == 'artistic':
            return 'librarys.reports_publishers_cards'
        else:
            return 'librarys.report_publisher_card'

    def _get_render_information(self):
        return {
            'docs': self.env['library.publisher'].search([], limit=1),
        }

    @api.depends('layout_choice')
    def _compute_preview(self):
        for wizard in self:
            try:
                template = wizard._get_preview_template()
                preview_html = wizard.env['ir.ui.view']._render_template(
                    template,
                    wizard._get_render_information()
                )
                wizard.preview = preview_html
            except Exception as e:
                _logger.error("Error rendering preview: %s", e)
                wizard.preview = "<p style='color:red;'>Preview could not be loaded.</p>"
