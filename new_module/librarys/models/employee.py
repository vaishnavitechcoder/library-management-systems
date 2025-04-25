from odoo import api, fields, models
from datetime import date, datetime


class LibraryEmployee(models.Model):
    _name = "library.employee"
    _description = "library employee"


    employee = fields.Many2one("hr.employee", string="Employee")
    company_id = fields.Many2one('res.company')
    company_country_id = fields.Many2one('res.country', 'Company Country', related='company_id.country_id', readonly=True)
    company_country_code = fields.Char(related='company_country_id.code', depends=['company_country_id'], readonly=True)
    # private info
    private_street = fields.Char(string="Private Street",  related="employee.private_street", store=True, readonly=False)
    private_street2 = fields.Char(string="Private Street2",related="employee.private_street2", store=True, readonly=False)
    private_city = fields.Char(string="Private City",related="employee.private_city", store=True, readonly=False)
    private_state_id = fields.Many2one(
        "res.country.state", string="Private State",
        domain="[('country_id', '=?', private_country_id)]")
    private_zip = fields.Char(string="Private Zip", related="employee.private_zip", store=True, readonly=False)
    private_country_id = fields.Many2one("res.country", string="Private Country")
    private_phone = fields.Char(string="Private Phone",related="employee.private_phone", store=True, readonly=False)
    private_email = fields.Char(string="Private Email",related="employee.private_email", store=True, readonly=False)
    country_id = fields.Many2one(
        'res.country', 'Nationality (Country)', )
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], )

    spouse_complete_name = fields.Char(string="Spouse Complete Name",related="employee.spouse_complete_name", store=True, readonly=False)
    spouse_birthdate = fields.Date(string="Spouse Birthdate",related="employee.spouse_birthdate", store=True, readonly=False)
    children = fields.Integer(string='Number of Dependent Children',related="employee.children", store=True, readonly=False)
    place_of_birth = fields.Char('Place of Birth',related="employee.place_of_birth", store=True, readonly=False)
    country_of_birth = fields.Many2one('res.country', string="Country of Birth")
    birthday = fields.Date('Date of Birth',related="employee.birthday", store=True, readonly=False)
    ssnid = fields.Char('SSN No', related="employee.ssnid", store=True, readonly=False)
    sinid = fields.Char('SIN No', related="employee.sinid", store=True, readonly=False)
    identification_id = fields.Char(string='Identification No', related="employee.identification_id", store=True, readonly=False)
    passport_id = fields.Char('Passport No', related="employee.passport_id", store=True, readonly=False)

    permit_no = fields.Char('Work Permit No',related="employee.permit_no", store=True, readonly=False )
    visa_no = fields.Char('Visa No', related="employee.visa_no", store=True, readonly=False)
    visa_expire = fields.Date('Visa Expiration Date',related="employee.visa_expire", store=True, readonly=False )
    work_permit_expiration_date = fields.Date('Work Permit Expiration Date',related="employee.work_permit_expiration_date", store=True, readonly=False )
    has_work_permit = fields.Binary(string="Work Permit",related="employee.has_work_permit", store=True, readonly=False)
    additional_note = fields.Text(string='Additional Note')
    certificate = fields.Selection([
        ('graduate', 'Graduate'),
        ('bachelor', 'Bachelor'),
        ('master', 'Master'),
        ('doctor', 'Doctor'),
        ('other', 'Other'),
    ], 'Certificate Level', )
    study_field = fields.Char("Field of Study", related="employee.study_field", store=True, readonly=False)
    study_school = fields.Char("School", related="employee.study_school", store=True, readonly=False)
    emergency_contact = fields.Char("Contact Name",related="employee.emergency_contact", store=True, readonly=False )
    emergency_phone = fields.Char("Contact Phone",related="employee.emergency_phone", store=True, readonly=False)
    distance_home_work = fields.Integer(string="Home-Work Distance",related="employee.distance_home_work", store=True, readonly=False)
    distance_home_work_unit = fields.Selection([
        ('kilometers', 'km'),
        ('miles', 'mi'),
    ], 'Home-Work Distance unit', default='kilometers', required=True)
    employee_type = fields.Selection([
            ('employee', 'Employee'),
            ('worker', 'Worker'),
            ('student', 'Student'),
            ('trainee', 'Trainee'),
            ('contractor', 'Contractor'),
            ('freelance', 'Freelancer'),
        ], string='Employee Type', default='employee', required=True,
        help="Categorize your Employees by type. This field also has an impact on contracts. Only Employees, Students and Trainee will have contract history.")


    # misc
    notes = fields.Text('Notes')
    color = fields.Integer('Color Index', default=0)
    barcode = fields.Char(string="Badge ID",related="employee.barcode", store=True, readonly=False, help="ID used for employee identification.", copy=False)
    pin = fields.Char(string="PIN", copy=False,related="employee.pin", store=True, readonly=False,
        help="PIN used to Check In/Out in the Kiosk Mode of the Attendance application (if enabled in Configuration) and to change the cashier in the Point of Sale application.")
    departure_reason_id = fields.Many2one("hr.departure.reason", string="Departure Reason",
                                          copy=False, ondelete='restrict')
    departure_description = fields.Html(string="Additional Information", related="employee.departure_description", store=True, readonly=False,copy=False)
    departure_date = fields.Date(string="Departure Date", related="employee.departure_date", store=True, readonly=False,copy=False)
    id_card = fields.Binary(string="ID Card Copy",related="employee.id_card", store=True, readonly=False)
    driving_license = fields.Binary(string="Driving License",related="employee.driving_license", store=True, readonly=False)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', readonly=True)

