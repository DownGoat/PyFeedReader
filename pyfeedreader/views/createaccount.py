__author__ = 'sis13'

from flask import *
import bcrypt
import time
from pyfeedreader.database import db_session
from pyfeedreader.models.user import User
from flask.ext.login import *
from pyfeedreader.forms.registrationform import RegistrationForm


mod = Blueprint('createaccount', __name__)


@mod.route("/createaccount", methods=["POST"])
def create_account():
    form = RegistrationForm(request.form)
    error = None

    if not form.validate():
        return render_template('createaccount.html', form=form)

    result = User.query.filter(User.username == form.username.data).first()
    if result:
        error = True
        form.username.errors = ["Username already in use."]

    result = User.query.filter(User.email == form.email.data).first()
    if result:
        error = True
        form.email.errors = ["E-Mail already in use."]

    if error:
        return render_template("createaccount.html", form=form)

    hash = bcrypt.hashpw(form.password.data, bcrypt.gensalt())

    user = User(email=form.email.data, password=hash, current_login=time.time(),
                last_login=time.time(), username=form.username.data)

    db_session.add(user)
    db_session.commit()

    #Login the user.
    login_user(user)

    return redirect("/")


@mod.route("/createaccount", methods=["GET"])
def display_ca_page():
    form = RegistrationForm(request.form)
    return render_template("createaccount.html", form=form)