__author__ = 'sis13'

from flask import *
from flask.ext.login import *

from pyfeedreader.database import fs_db_session


mod = Blueprint('index', __name__)


@mod.route("/", methods=["GET"])
@login_required
def index():
    current_user.feed_entities(fs_db_session)
    u = current_user
    return render_template("index.html",    entries=current_user.entries[:10],
                                            dirs=current_user.dirs,
                                            feeds=current_user.rfeed
                            )