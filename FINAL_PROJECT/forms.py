from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, ValidationError, PasswordField, IntegerField
from wtforms.validators import DataRequired, EqualTo
from wtforms_sqlalchemy.fields import QuerySelectField
import app


def group_query():
    return app.Group.query


class BillForm(FlaskForm):
    description = StringField('Description', [DataRequired()])
    amount = IntegerField('Amount $', [DataRequired()])
    group = QuerySelectField(query_factory=group_query, allow_blank=False,
                             get_label="name", get_pk=lambda obj: str(obj))
    submit = SubmitField('Confirm')


class GroupForm(FlaskForm):
    name = StringField('Group Name', [DataRequired()])
    submit = SubmitField('Confirm')


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


class GetGroupForm(FlaskForm):
    id = IntegerField('Get Group By Id', [DataRequired()])
    submit = SubmitField("Confirm")
