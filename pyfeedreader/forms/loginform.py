import bcrypt
from pyfeedreader import User

__author__ = 'sis13'

from wtforms import Form, BooleanField, TextField, PasswordField, validators


class LoginForm(Form):
    username = TextField('Username', [
        validators.Required("You must enter a username."),
    ])

    password = PasswordField('Password', [
        validators.Required("You must enter a password."),
    ])

    remember_me = BooleanField("Remember me", default=True)

    def valid_login(self, form, username, password):
        user = User.query.filter(User.username == username).first()
        if not user:
            return False

        if bcrypt.hashpw(password, user.password) != user.password:
            return False

        return user