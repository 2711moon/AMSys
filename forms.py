from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SubmitField, SelectField, IntegerField, DecimalField, DateField
)
from wtforms.validators import DataRequired, Optional, Length, Regexp, NumberRange

class CSRFOnlyForm(FlaskForm):
    pass

class LoginForm(FlaskForm):
    identifier = StringField('Username', validators=[DataRequired()])
    passcode = PasswordField('Password', validators=[DataRequired()])

class AssetForm(FlaskForm):
    # Asset Type
    category = SelectField('Asset Type', choices=[
        ('mobile', 'Mobile'),
        ('barcode_scanner', 'Barcode Scanner'),
        ('face_machine', 'Face Machine'),
        ('franchise_tab', 'Franchise TAB'),
        ('frchs_printer', 'FRCHS-Printer'),
        ('franchise_inv', 'Franchise Inv'),
        ('laptop', 'Laptop'),
        ('faulty_laptops', 'Faulty Laptops'),
        ('ip_phones', 'IP Phones'),
        ('printer', 'Printer'),
        ('desktop', 'Desktop'),
        ('all_in_one', 'All-in-one'),
        ('online', 'Online'),
        ('mouse_kbd', 'Mouse - KBD'),
        ('hdd', 'HDD'),
        ('add_new_type', 'Add New Type')
    ], validators=[DataRequired()])

    # Optional: Add New Type
    new_type = StringField('Add New Type', validators=[Optional(), Length(max=50)])

    # Asset Name
    name = StringField('Asset Name', validators=[DataRequired(), Length(max=100)])

    # Status
    status = SelectField('Status', choices=[
        ('available', 'Available'),
        ('assigned', 'Assigned'),
        ('maintenance', 'Maintenance')
    ], validators=[DataRequired()])

    # Dynamic Fields
    third_party_code = IntegerField('Third Party Code', validators=[Optional()])
    user_code = IntegerField('User Code', validators=[Optional()])
    area = StringField('Area', validators=[Optional()])
    username = StringField('Username', validators=[Optional()])

    # ✅ Date fields updated to match <input type="date"> format
    given_date = DateField('Given Date (YYYY-MM-DD)', format='%Y-%m-%d', validators=[Optional()])
    owner = StringField('Owner',validators=[Optional(), Regexp(r'^[A-Za-z ]*$', message='Owner name must contain only letters and spaces.')]) 

    license = StringField('License', validators=[Optional()])
    os = StringField('Operating System', validators=[Optional()])
    system = StringField('System', validators=[Optional()])
    system_manufacturer = StringField('System Manufacturer', validators=[Optional()])
    serial_no = StringField('Serial Number', validators=[Optional()])
    processor = StringField('Processor', validators=[Optional()])
    ram = IntegerField('RAM (GB)', validators=[Optional()])
    harddisk = StringField('Hard Disk', validators=[Optional()])

    # ✅ Specification choices title-cased to match HTML options
    specification = SelectField('Specification', choices=[
        ('refurbished', 'Refurbished'),
        ('new', 'New')
    ], validators=[Optional()])

    purchase_date= DateField('Date of Purchase (YYYY-MM-DD)', format='%Y-%m-%d', validators=[Optional()])
    vendor = StringField('Vendor', validators=[Optional()])
    invoice_no = IntegerField('Invoice Number', validators=[Optional()])
    amount = StringField('Amount (e.g. ₹5000 ($60))', validators=[Optional(), Length(max=50)])

    # Remarks
    remarks = StringField('Remarks', validators=[Optional(), Length(max=500)])

    # Submit Button
    submit = SubmitField('Submit')
