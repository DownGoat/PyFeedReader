from pyfeedreader.forms.loginform import LoginForm

__author__ = 'sis13'
from flask import *
import bcrypt
import random
import time
from pyfeedreader import app
from pyfeedreader.database import db_session
from pyfeedreader.models.user import User
from flask.ext.login import (LoginManager, current_user, login_required,
                             login_user, logout_user, UserMixin, AnonymousUser,
                             confirm_login, fresh_login_required)


mod = Blueprint('login', __name__)

@mod.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)

    if request.method == "GET":
        return render_template("login.html", form=form)

    if not form.validate():
        return render_template("login.html", form=form)

    user = form.valid_login(form, form.username.data, form.password.data)
    if not user:
        form.username.errors = ["The login details provided are not correct."]

        return render_template("login.html", form=form)

    flash("Logged in successfully.")
    login_user(user)

    return redirect("/")
