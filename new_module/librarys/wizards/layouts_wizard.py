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

    @api.depends('layout_choice','logo', 'font', 'primary_color', 'secondary_color', 'report_header', 'report_footer', 'layout_background', 'layout_background_image', 'company_details')
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

    @api.model
    def _default_report_footer(self):
        company = self.env.company
        footer_fields = [field for field in [company.phone, company.email, company.website, company.vat] if
                         isinstance(field, str) and len(field) > 0]
        return Markup(' ').join(footer_fields)

    @api.model
    def _default_company_details(self):
        company = self.env.company
        address_format, company_data = company.partner_id._prepare_display_address()
        address_format = self._clean_address_format(address_format, company_data)
        # company_name may *still* be missing from prepared address in case commercial_company_name is falsy
        if 'company_name' not in address_format:
            address_format = '%(company_name)s\n' + address_format
            company_data['company_name'] = company_data['company_name'] or company.name
        return nl2br(address_format) % company_data

    def _clean_address_format(self, address_format, company_data):
        missing_company_data = [k for k, v in company_data.items() if not v]
        for key in missing_company_data:
            if key in address_format:
                address_format = address_format.replace(f'%({key})s\n', '')
        return address_format

    company_id = fields.Many2one(
        'res.company', default=lambda self: self.env.company, required=True)

    logo = fields.Binary(related='company_id.logo', readonly=False)
    preview_logo = fields.Binary(related='logo', string="Preview logo")
    report_header = fields.Html(related='company_id.report_header', readonly=False)
    report_footer = fields.Html(related='company_id.report_footer', readonly=False, default=_default_report_footer)
    company_details = fields.Html(related='company_id.company_details', readonly=False,
                                  default=_default_company_details)
    is_company_details_empty = fields.Boolean(compute='_compute_empty_company_details')

    # The paper format changes won't be reflected in the preview.
    paperformat_id = fields.Many2one(related='company_id.paperformat_id', readonly=False)


    font = fields.Selection(related='company_id.font', readonly=False)
    primary_color = fields.Char(related='company_id.primary_color', readonly=False)
    secondary_color = fields.Char(related='company_id.secondary_color', readonly=False)

    custom_colors = fields.Boolean(compute="_compute_custom_colors", readonly=False)
    logo_primary_color = fields.Char(compute="_compute_logo_colors")
    logo_secondary_color = fields.Char(compute="_compute_logo_colors")

    layout_background = fields.Selection(related='company_id.layout_background', readonly=False)
    layout_background_image = fields.Binary(related='company_id.layout_background_image', readonly=False)

    # Those following fields are required as a company to create invoice report
    partner_id = fields.Many2one(related='company_id.partner_id', readonly=True)
    phone = fields.Char(related='company_id.phone', readonly=True)
    email = fields.Char(related='company_id.email', readonly=True)
    website = fields.Char(related='company_id.website', readonly=True)
    vat = fields.Char(related='company_id.vat', readonly=True)
    name = fields.Char(related='company_id.name', readonly=True)
    country_id = fields.Many2one(related="company_id.country_id", readonly=True)

    @api.depends('logo_primary_color', 'logo_secondary_color', 'primary_color', 'secondary_color', )
    def _compute_custom_colors(self):
        for wizard in self:
            logo_primary = wizard.logo_primary_color or ''
            logo_secondary = wizard.logo_secondary_color or ''
            # Force lower case on color to ensure that FF01AA == ff01aa
            wizard.custom_colors = (
                    wizard.logo and wizard.primary_color and wizard.secondary_color
                    and not (
                    wizard.primary_color.lower() == logo_primary.lower()
                    and wizard.secondary_color.lower() == logo_secondary.lower()
            )
            )

    @api.depends('logo')
    def _compute_logo_colors(self):
        for wizard in self:
            if wizard._context.get('bin_size'):
                wizard_for_image = wizard.with_context(bin_size=False)
            else:
                wizard_for_image = wizard
            wizard.logo_primary_color, wizard.logo_secondary_color = wizard.extract_image_primary_secondary_colors(
                wizard_for_image.logo)

    @api.onchange('custom_colors')
    def _onchange_custom_colors(self):
        for wizard in self:
            if wizard.logo and not wizard.custom_colors:
                wizard.primary_color = wizard.logo_primary_color or DEFAULT_PRIMARY
                wizard.secondary_color = wizard.logo_secondary_color or DEFAULT_SECONDARY

    @api.onchange('logo')
    def _onchange_logo(self):
        for wizard in self:
            # It is admitted that if the user puts the original image back, it won't change colors
            company = wizard.company_id
            # at that point wizard.logo has been assigned the value present in DB
            if wizard.logo == company.logo and company.primary_color and company.secondary_color:
                continue

            if wizard.logo_primary_color:
                wizard.primary_color = wizard.logo_primary_color
            if wizard.logo_secondary_color:
                wizard.secondary_color = wizard.logo_secondary_color

    @api.model
    def extract_image_primary_secondary_colors(self, logo, white_threshold=225, mitigate=175):
        """
        Identifies dominant colors

        First resizes the original image to improve performance, then discards
        transparent colors and white-ish colors, then calls the averaging
        method twice to evaluate both primary and secondary colors.

        :param logo: logo to process
        :param white_threshold: arbitrary value defining the maximum value a color can reach
        :param mitigate: arbitrary value defining the maximum value a band can reach

        :return colors: hex values of primary and secondary colors
        """
        if not logo:
            return False, False
        # The "===" gives different base64 encoding a correct padding
        logo += b'===' if isinstance(logo, bytes) else '==='
        try:
            # Catches exceptions caused by logo not being an image
            image = tools.image_fix_orientation(tools.base64_to_image(logo))
        except Exception:
            return False, False

        base_w, base_h = image.size
        w = int(50 * base_w / base_h)
        h = 50

        # Converts to RGBA (if already RGBA, this is a noop)
        image_converted = image.convert('RGBA')
        image_resized = image_converted.resize((w, h), resample=Resampling.NEAREST)

        colors = []
        for color in image_resized.getcolors(w * h):
            if not (color[1][0] > white_threshold and
                    color[1][1] > white_threshold and
                    color[1][2] > white_threshold) and color[1][3] > 0:
                colors.append(color)

        if not colors:  # May happen when the whole image is white
            return False, False
        primary, remaining = tools.average_dominant_color(colors, mitigate=mitigate)
        secondary = tools.average_dominant_color(remaining, mitigate=mitigate)[0] if remaining else primary

        # Lightness and saturation are calculated here.
        # - If both colors have a similar lightness, the most colorful becomes primary
        # - When the difference in lightness is too great, the brightest color becomes primary
        l_primary = tools.get_lightness(primary)
        l_secondary = tools.get_lightness(secondary)
        if (l_primary < 0.2 and l_secondary < 0.2) or (l_primary >= 0.2 and l_secondary >= 0.2):
            s_primary = tools.get_saturation(primary)
            s_secondary = tools.get_saturation(secondary)
            if s_primary < s_secondary:
                primary, secondary = secondary, primary
        elif l_secondary > l_primary:
            primary, secondary = secondary, primary

        return tools.rgb_to_hex(primary), tools.rgb_to_hex(secondary)

    def document_layout_save(self):
        # meant to be overridden
        return self.env.context.get('report_action') or {'type': 'ir.actions.act_window_close'}

    def _get_asset_style(self):
        """
        Compile the style template. It is a qweb template expecting company ids to generate all the code in one batch.
        We give a useless company_ids arg, but provide the PREVIEW_ID arg that will prepare the template for
        '_get_css_for_preview' processing later.
        :return:
        """
        company_styles = self.env['ir.qweb']._render('web.styles_company_report', {
            'company_ids': self,
        }, raise_if_not_found=False)

        return company_styles

    @api.model
    def _compile_scss(self, scss_source):
        """
        This code will compile valid scss into css.
        Parameters are the same from odoo/addons/base/models/assetsbundle.py
        Simply copied and adapted slightly
        """

        # No scss ? still valid, returns empty css
        if not scss_source.strip():
            return ""

        precision = 8
        output_style = 'expanded'
        bootstrap_path = file_path('web/static/lib/bootstrap/scss')

        try:
            compiled_css = libsass.compile(
                string=scss_source,
                include_paths=[
                    bootstrap_path,
                ],
                output_style=output_style,
                precision=precision,
            )
            return Markup(compiled_css) if isinstance(compiled_css, Markup) else compiled_css
        except libsass.CompileError as e:
            raise libsass.CompileError(e.args[0])

    @api.depends('company_details')
    def _compute_empty_company_details(self):
        # In recent change when an html field is empty a <p> balise remains with a <br> in it,
        # but when company details is empty we want to put the info of the company
        for record in self:
            record.is_company_details_empty = not html2plaintext(record.company_details or '')