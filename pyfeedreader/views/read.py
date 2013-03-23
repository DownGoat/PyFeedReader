from pyfeedreader.forms.directoryforms import NewDirForm, AddFeedDirForm
from pyfeedreader.models.ReadEntries import ReadEntry
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


mod = Blueprint('read', __name__)

@mod.route("/read", methods=["POST"])
@login_required
def read_entry():
    if not request.form.get("entry_id", None):
        return redirect("/")

    entry_id = request.form.get("entry_id", None)

    read_entry = ReadEntry(entry_id=entry_id, user_id=current_user.id)
    db_session.add(read_entry)
    db_session.commit()

    return redirect("/", code=200)