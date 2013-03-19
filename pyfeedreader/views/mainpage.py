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


mod = Blueprint('index', __name__)

@mod.route("/", methods=["GET"])
@login_required
def index():
    return render_template("index.html")