from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired


class SignUpForm(FlaskForm):
    inputFirstName = StringField('First Name',
        [DataRequired(message="Please enter your first name !")])
    inputLastName = StringField('Last Name',
        [DataRequired(message="Please enter your last name !")])
    inputEmail = StringField('Email address',
        [Email(message="Not a valid email address!"),
        DataRequired(message="Please enter your email address")])
    inputPassword = PasswordField('Password',
        [InputRequired(message="Please enter password!"),
         EqualTo('inputConfirmPassword', message="Password does not match!")])
    inputConfirmPassword = PasswordField('Confirm password')
    submit = SubmitField('Sign Up')


class AddProjectForm(FlaskForm):
    inputName = StringField('Name', [InputRequired(message="Please enter your project name!")])
    inputDescription = StringField('Description', [InputRequired(message="Please enter your description!")])
    inputDeadline = DateTimeLocalField('Deadline', format='%Y-%m-%dT%H:%M', validators=[InputRequired(message="Please enter your project deadline!")])


class SignInForm(FlaskForm):
    inputEmail = StringField('Email address',
        [Email(message="Not a valid email address!"),
        DataRequired(message="Please enter your email address!")])
    inputPassword = PasswordField('Password',
        [InputRequired(message="Please enter your passsword!")])
    submit = SubmitField('Sign In')


class TaskForm(FlaskForm):
    inputDescription = StringField('Task Description', [DataRequired(message="Please enter your task content")])
    inputDeadLine = DateTimeLocalField('Deadline', format='%Y-%m-%dT%H:%M', validators=[InputRequired(message="Please enter your Task deadline!")])

    inputPriority = SelectField('Priority', coerce=int)
    inputProject = SelectField('Project', coerce=int)
    inputStatus = SelectField('Status', coerce=int)
