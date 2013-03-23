__author__ = 'sis13'

from flask import *
import bcrypt
import random
import time
from pyfeedreader import app
from pyfeedreader.database import db_session, fs_db_session
from pyfeedreader.models.user import User
from flask.ext.login import *
from pyfeedreader.models.entry import Entry
from pyfeedreader.models.feed import Feed


mod = Blueprint('index', __name__)


@mod.route("/", methods=["GET"])
@login_required
def index():

    current_user.feed_entities(fs_db_session)

    u = current_user

    return render_template("index.html", entries=current_user.entries, dirs=current_user.dirs)