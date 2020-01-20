from flask_wtf import FlaskForm
from wtforms import FileField, StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import InputRequired, Email


class UploadForm(FlaskForm):
    file = FileField(validators=[InputRequired()])
    projects = SelectField('Project', coerce=int, validators=[InputRequired()])


class LogInForm(FlaskForm):
    email = StringField('Email', validators=[Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    login = SubmitField('Log in')


class SignUpForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_password = PasswordField('Confirm password', validators=[InputRequired()])
    companies = SelectField('Company', coerce=int, validators=[InputRequired()])
    secret_key = PasswordField('Secret company key', validators=[InputRequired()])


class ChangeForm(FlaskForm):
    old_password = PasswordField('Old_password', validators=[InputRequired()])
    new_password = PasswordField('New_password', validators=[InputRequired()])
    confirm_password = PasswordField('Confirm_password', validators=[InputRequired()])


class FilterForm(FlaskForm):
    filter = StringField('Filter name')


class CompanyForm(FlaskForm):
    name = StringField('Name of company', validators=[InputRequired()])
    secret_key = StringField('Secret key', validators=[InputRequired()])
    website = StringField('Website')
    email = StringField('Email', validators=[InputRequired(), Email()])
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_password = PasswordField('Confirm password', validators=[InputRequired()])


class ProjectForm(FlaskForm):
    name = StringField('Name of project', validators=[InputRequired()])
    description = StringField('Description')
