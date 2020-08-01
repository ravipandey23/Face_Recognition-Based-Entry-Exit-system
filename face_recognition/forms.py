from flask_wtf import FlaskForm
import string
from flask import flash
from wtforms import StringField, PasswordField, SubmitField, BooleanField,IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
#from security.models import User
import re

class student_registration(FlaskForm):
    name = StringField('Name',validators=[DataRequired()])
    enrol_number = StringField('Enrollment Number',validators=[DataRequired()])
    contact = StringField('Contact Number',validators=[DataRequired()])
    parent_contact = StringField('Parents Contact', validators=[DataRequired()])
    room_number = StringField('Room Number',validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate(self):
        enroll = self.enrol_number.data
        check_enrol = self.validate_enrol(enroll)
        check_contact = self.validate_contact(self.contact.data)
        check_par = self.validate_par_contact(self.parent_contact.data)
        if(check_enrol and check_contact and check_par):
            return True
        else:
            return False

    def validate_enrol(self,enroll):
        if(len(enroll)!=10):
            flash(f'Invalid Enrolment Length', 'danger')
            return False
        if(enroll[0].isalpha() and enroll[1].isalpha() and enroll[2].isalpha() and enroll[3].isdigit() and enroll[4].isdigit() and enroll[5].isdigit() and enroll[6].isdigit() and enroll[7].isdigit() and enroll[8].isdigit() and enroll[9].isdigit()):
            return True
        else:
            flash(f'Invalid Enrolment Number', 'danger')
            return False

    def validate_contact(self,contac):
        if(len(contac)!=10):
            flash(f"Invalid Contact Length", 'danger')
            return False
        rule = re.compile(r'^(?:\+?91)?[9876]\d{9}$')
        if not rule.search(contac):
            flash(f"Invalid Contact Number", 'danger')
            return False
        return True

    def validate_par_contact(self,contac):
        if(len(contac)!=10):
            flash(f"Invalid Parent's Contact Length", 'danger')
            return False
        rule = re.compile(r'^(?:\+?91)?[9876]\d{9}$')
        if not rule.search(contac):
            flash(f"Invalid Parent's Contact Number", 'danger')
            return False
        return True

class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')   

class Hostel_entry(FlaskForm):
    destination = StringField('Destination',validators=[DataRequired()])
    submit = SubmitField('Submit')

class New_Room(FlaskForm):
    enrol = StringField('Enrolment Number',validators=[DataRequired()])
    new_room = StringField('New Room', validators=[DataRequired()])
    submit = SubmitField('Update')   

class New_Contact(FlaskForm):
    enrol = StringField('Enrolment Number',validators=[DataRequired()])
    new_contact = StringField('New Contact', validators=[DataRequired()])
    submit = SubmitField('Update')

    def validate(self):
        check_contact = self.validate_contact(self.new_contact.data)
        if(check_contact):
            return True
        else:
            return False

    def validate_contact(self,contac):
        if(len(contac)!=10):
            flash(f"Invalid Contact Length", 'danger')
            return False
        rule = re.compile(r'^(?:\+?91)?[9876]\d{9}$')
        if not rule.search(contac):
            flash(f"Invalid Contact Number", 'danger')
            return False
        return True

class Parent_new_contact(FlaskForm):
    enrol = StringField('Enrolment Number',validators=[DataRequired()])
    parent_new_contact = StringField("Parent's New Contact", validators=[DataRequired()])
    submit = SubmitField('Update')

    def validate(self):
        check_par_contact = self.validate_par_contact(self.parent_new_contact.data)
        if(check_par_contact):
            return True
        else:
            return False

    def validate_par_contact(self,contac):
        if(len(self.parent_new_contact.data)!=10):
            flash(f"Invalid Parent's Contact Length", 'danger')
            return False
        rule = re.compile(r'^(?:\+?91)?[9876]\d{9}$')
        if not rule.search(self.parent_new_contact.data):
            flash(f"Invalid Parent's Contact Number", 'danger')
            return False
        return True

class Single_student(FlaskForm):
    enrol = StringField('Enrolment Number',validators=[DataRequired()])
    submit = SubmitField('Delete')

class Input_enrol(FlaskForm):
    enrol = StringField('Enrolment Number',validators=[DataRequired()])
    submit = SubmitField('Submit')

class Batch(FlaskForm):
    batch = StringField('Batch Year',validators=[DataRequired()])
    submit = SubmitField('Delete')

class Input_date(FlaskForm):
    date = StringField('Date',validators=[DataRequired()], render_kw={"placeholder":"YYYY-MM-DD"})
    submit = SubmitField('Submit')

    