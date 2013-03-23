from pyfeedreader.forms.directoryforms import NewDirForm, AddFeedDirForm
from pyfeedreader.models.directory import Directory
from pyfeedreader.models.direntries import DirEntry

__author__ = 'sis13'

from flask import *
import bcrypt
import random
import time

from pyfeedreader.forms.loginform import LoginForm
from pyfeedreader import app
from pyfeedreader.database import db_session
from pyfeedreader.models.user import User
from flask.ext.login import *


mod = Blueprint('directory', __name__)

@mod.route("/directory/new", methods=["POST"])
@login_required
def new_dir():
    form = NewDirForm(request.form)

    if not form.validate():
        return render_template("index.html", entries=[], dirs=current_user.dirs)

    dir = Directory(name=form.name.data, user_id=current_user.id)
    db_session.add(dir)
    db_session.commit()

    return redirect("/")

@mod.route("/directory/add/feed", methods=["POST"])
@login_required
def add_feed_dir():
    form = AddFeedDirForm(request.form)
    if not form.validate():
        return render_template("index.html", entries=[], dirs=current_user.dirs)

    de = DirEntry(feed_id=form.feed_id.data, dir_id=form.dir_id.data)
    db_session.add(de)
    db_session.commit()

    return redirect("/")