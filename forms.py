from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, StringField, PasswordField
from wtforms.validators import DataRequired, ValidationError, EqualTo
import app


class RegisterForm(FlaskForm):
    name = StringField('Name', [DataRequired()])
    email = StringField('Email', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    confirmed_password = PasswordField(
        "Please confirm your password", [EqualTo('password', 'Your password does not match')])
    submit = SubmitField("Register")

    def validate_name(self, name):
        user = app.User.query.filter_by(name=name.data).first()
        if user:
            raise ValidationError(
                'This name is already used, please choose another')


class LoginForm(FlaskForm):
    email = StringField('Email', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    remember = BooleanField("Remember me")
    submit = SubmitField('Login')
