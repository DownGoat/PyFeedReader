__author__ = 'sis13'

from wtforms import Form, BooleanField, TextField, PasswordField, validators


class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=25)])
    email = TextField('E-Mail Address', [
        validators.Length(min=6, max=100),
        validators.Required(),
        validators.EqualTo("emailc", message="E-Mails must match.")
    ])

    emailc = TextField("Repeate E-Mail", [
        validators.Length(min=6, max=100),
        validators.Required(),
        validators.EqualTo("email", message="")
    ])

    password = PasswordField('New Password', [
        validators.Length(min=6, max=1024),
        validators.Required(),
        validators.EqualTo('passwc', message='Passwords must match.')
    ])

    passwc = PasswordField('Repeat Password', [
        validators.Length(min=6, max=1024),
        validators.Required(),
        validators.EqualTo('password', message="")
    ])

