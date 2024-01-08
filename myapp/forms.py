from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField, FloatField, DateField, RadioField
from wtforms.validators import (DataRequired, Email, EqualTo, Length, Optional, Regexp, ValidationError)
from flask_wtf.file import FileField, FileRequired, FileAllowed
from datetime import datetime


class LoginForm(FlaskForm):
        """
    This class creates a user login form

            Parameters:
                    username (StringField): A single line of text for user to input name
                    password (PasswordField): A single line of text for users to enter password
                    remember_me (BooleanField): a checkbox
                    submit (SubmitField)

            Returns:
                    Show a login form
    """
        __tablename__ = 'users'
        username = StringField('Username', validators=[DataRequired()])
        password = PasswordField('Password', validators=[DataRequired()])
        remember_me = BooleanField('Remember me', default=False)
        submit = SubmitField('Log In')

class SignupForm(FlaskForm):
        """
         This class creates a user signup form

            Parameters:
                    username (StringField): A single line of text for user to input name
                    email (StringField): A single line of text for users to input email
                    password (PasswordField): A single line of text for users to enter password
                    confirm (PasswordFeild): A single line of text for users to re-enter password
                    submit (SubmitField)

            Returns:
                    Show a signup form
        """
        username = StringField('Username', validators=[DataRequired()])
        email = StringField('Email', validators=[DataRequired()])
        password = PasswordField('Password', validators=[DataRequired(), Length(min=6, message='Select a stronger password.')])
        confirm = PasswordField('Confirm yor password', validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])
        submit = SubmitField('Register')


class AgencySignupForm(FlaskForm):
        """
         This class creates a user signup form

            Parameters:
                    username (StringField): A single line of text for user to input name
                    email (StringField): A single line of text for users to input email
                    password (PasswordField): A single line of text for users to enter password
                    confirm (PasswordFeild): A single line of text for users to re-enter password
                    submit (SubmitField)

            Returns:
                    Show a signup form
        """
        username = StringField('Username', validators=[DataRequired()])
        email = StringField('Email', validators=[DataRequired()])
        password = PasswordField('Password', validators=[DataRequired(), Length(min=6, message='Select a stronger password.')])
        confirm = PasswordField('Confirm yor password', validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])
        submit = SubmitField('Register')

class EditPicture(FlaskForm):
    picture = FileField(label="Add Profile Photo", validators=[FileAllowed(['jpg','png']), FileRequired()])
    submit = SubmitField('Save Changes')

class EditProfile(FlaskForm):

    first = StringField('First Name')
    last = StringField('Last Name')
    phone = StringField('Phone Number')
    address1 = StringField('Address Line 1')
    address2 = StringField('Address Line 2')
    postal = StringField('Enter Postal Code', validators=[Length(min=5,max=5, message="Postal Code must be valid"), Regexp('\d{5}', message='No Good' )])
    state = SelectField('State', choices = ['Alabama','Alaska','Arizona','Arkansas','California','Colorado','Connecticut','Delaware','Florida','Georgia','Hawaii','Idaho','Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana','Maine','Maryland','Massachusetts','Michigan','Minnesota','Mississippi','Missouri','Montana','Nebraska','Nevada','New Hampshire','New Jersey','New Mexico','New York','North Carolina','North Dakota','Ohio','Oklahoma','Oregon','Pennsylvania','Rhode Island','South Carolina','South Dakota','Tennessee','Texas','Utah','Vermont','Virginia','Washington','West Virginia','Wisconsin','Wyoming'])
    submit = SubmitField('Save Changes')


class ListingForm(FlaskForm):
    picture = FileField(label="Add Item Photo", validators=[FileAllowed(['jpg','png']), FileRequired()])
    name = StringField('Item Name', validators=[DataRequired()])
    description = StringField('Item Description')
    location = StringField('Enter Postal Code', validators=[DataRequired(), Length(min=5,max=5, message="Postal Code must be valid"), Regexp('\d{5}', message='Enter a valid Postal Code' )])

    agency = SelectField('Enter Agency', choices=[], default='None', render_kw={"placeholder": "None"})
    warehouse = BooleanField('Add Premium Warehouse?')
    free = BooleanField('List Item As Free')
    price = FloatField('Item Price (leave blank if free)', validators=[Optional()])
    trade = BooleanField('List Item For Trade')
    submit = SubmitField('Create Listing')

    def validate_location(self, location):
        excluded_chars = "[a-zA-Z]*?!'^+%&/()=}][{$#"
        for char in self.location.data:
            if char in excluded_chars:
                raise ValidationError(
                    f"Letters are not allowed in postal code.")


class VolunteerForm(FlaskForm):
    picture = FileField(label="Add Item Photo", validators=[FileAllowed(['jpg','png']), FileRequired()])
    name = StringField('Volunteer Opportunity Name', validators=[DataRequired()])
    description = StringField('Opportunity Description')
    location = StringField('Enter Postal Code', validators=[DataRequired(), Length(min=5,max=5, message="Postal Code must be valid"), Regexp('\d{5}', message='Enter a valid Postal Code' )])
    date = DateField('Enter Event Date', id='datepick', validators=[DataRequired()])
    submit = SubmitField('Create Opportunity')

    def validate_date(form, date):
        right_now = datetime.now()
        right = datetime.date(right_now)
        if date.data < right:
            raise ValidationError("The date you have entered has already passed")


class NewName(FlaskForm):
    name = StringField("Enter New Name")
    submit = SubmitField("Save Changes")

class NewDesc(FlaskForm):
    desc = StringField("Enter New Description")
    submit = SubmitField("Save Changes")

class NewPrice(FlaskForm):
    price = FloatField("Enter New Price")
    submit = SubmitField("Save Changes")


class ReviewForm(FlaskForm):
    rating = RadioField('Give Seller Rating:', choices=[('5','5'),('4','4'),('3','3'),('2', '2'), ('1', '1')])
    review = StringField("Give Seller Review: ")
    submit = SubmitField("Submit Rating")

class ReportForm(FlaskForm):
    reason = StringField("Reason For Reporting")
    submit = SubmitField("Submit")

class Adddonations(FlaskForm):

    phone = StringField('Contact Number')

    account = StringField('Account Number',validators=[DataRequired(message='Please Enter a Valid account number'), Length(min=10, max=10, message='An account number should be 10 digits' ), Regexp('\d{10}', message='Enter a valid Account Number' )])
    date = DateField("Issue Date", validators=[DataRequired(message='Please enter a valid date')])
    submit = SubmitField('Add Donations')

class ChangePassword(FlaskForm):
    password = PasswordField('Enter Old Password', validators=[DataRequired()])
    newpassword = PasswordField('Enter New Password', validators=[DataRequired(), Length(min=6, message='Select a stronger password.')])
    confirm = PasswordField('Confirm your new password', validators=[DataRequired(), EqualTo('newpassword', message='Passwords must match.')])
    submit = SubmitField('Change Password')


class SearchForm(FlaskForm):
    search = StringField("Search Listings")
    submit = SubmitField("Submit")

class SendMessageForm(FlaskForm):

    sent_id = StringField('Send to', validators=[DataRequired()])
    content = StringField('Content', validators=[DataRequired(), Length(min=2, message='Message should be longer than 1 character')])
    submit = SubmitField('Send Message')

class SearchMessageForm(FlaskForm):

    search = StringField('Please enter username to access message history', validators=[DataRequired()])
    submit = SubmitField('Search')

class ProfileMessage(FlaskForm):
    content = StringField("Message:")
    submit = SubmitField("Send")

class SendMsgForm(FlaskForm):
    content = StringField('Content', validators=[DataRequired(), Length(min=2, message='Message should be longer than 1 character')])
    submit = SubmitField('Send Message')
