from pyfeedreader.forms.registrationform import RegistrationForm

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


mod = Blueprint('createaccount', __name__)


@mod.route("/createaccount", methods=["POST"])
def create_account():
    form = RegistrationForm(request.form)

    if not form.validate():
        return render_template('createaccount.html', form=form)

    result = User.query.filter(User.username == form.username.data).first()
    if result:
        form.username.errors = ["Username already in use."]

    result = User.query.filter(User.email == form.email.data).first()
    if result:
        form.email.errors = ["E-Mail already in use."]

    if result:
        return render_template("createaccount.html", form=form)

    hash = bcrypt.hashpw(form.password.data, bcrypt.gensalt())

    user = User(form.email.data, hash, None, time.time(), time.time(), form.username.data)
    db_session.add(user)
    db_session.commit()

    login_user(user)

    return redirect("/")


@mod.route("/createaccount", methods=["GET"])
def display_ca_page():
    form = RegistrationForm(request.form)
    return render_template("createaccount.html", form=form)