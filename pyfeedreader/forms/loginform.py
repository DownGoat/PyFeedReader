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
        """
        Validates the login form by checking that username and password match what is in the DB.

        :param form: Not used
        :param username:
        :param password:
        :return: Returns False if the login details are not correct, returns True otherwise.
        """
        user = User.query.filter(User.username == username).first()
        if not user:
            return False

        if bcrypt.hashpw(password, user.password) != user.password:
            return False

        return user