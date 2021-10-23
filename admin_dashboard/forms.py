from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,RadioField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired,Email,EqualTo,Length, Regexp
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed
from admin_dashboard.models import UsersDB

class LoginForm(FlaskForm):

    email=StringField('Email',validators=[DataRequired(),Email(message="Not a valid Email Format.")])
    password=PasswordField('Password ',validators=[DataRequired(),Length(4,10,'Password must be between 4-10 characters')])
    account_type = SelectField(u'Account Type ', choices=[('Normal', 'Normal'), ('Admin', 'Admin')])
    submit=SubmitField('Log In!')

class RegistrationForm(FlaskForm):

    f_name=StringField('Full Name ',validators=[DataRequired()])
    email=StringField('Email ',validators=[DataRequired(),Email(message="Not a valid Email Format.")])
    username=StringField('Username ',validators=[DataRequired()])
    password=PasswordField('Password ',validators=[DataRequired(),EqualTo('pass_confirm'),
            Length(4,10,'Password must be between 4-10 characters')])
    pass_confirm=PasswordField('Confirm Password ',validators=[DataRequired()])
    picture=FileField('Profile Image ',validators=[FileAllowed(['jpg','png','jpeg'])])
    gender = RadioField('Gender ',choices=[('M','Male'),('F','Female')])
    education = SelectField(u'Highest Education ', choices=[('Masters', 'Masters'), ('Bachelors', 'Bachelors'),
                 ('Diploma', 'Diploma')])

    hobbies = SelectMultipleField(u'Hobbies ', choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')])
    submit=SubmitField('Register Me!')

    def validate_email(self,email):
        if UsersDB().getUser(self.email.data):
            raise ValidationError('Your Email has already been registered!')

    def validate_username(self,username):
        if UsersDB().getUserByUserName(self.username.data):
            raise ValidationError('Your username has already been registered!')

class UpdateAccount(FlaskForm):
    profile_image=FileField('Profile Image ',validators=[FileAllowed(['jpg','png','jpeg'])])
    submit=SubmitField('Update Image')