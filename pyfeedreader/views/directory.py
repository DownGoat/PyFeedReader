from pyfeedreader.forms.directoryforms import NewDirForm, AddFeedDirForm
from pyfeedreader.models.directory import Directory
from pyfeedreader.models.direntries import DirEntry
from pyfeedreader.models.userfeeds import UserFeeds

__author__ = 'sis13'

from flask import *

from pyfeedreader.database import db_session
from flask.ext.login import *


mod = Blueprint('directory', __name__)

@mod.route("/directory/new", methods=["POST"])
@login_required
def new_dir():
    form = NewDirForm(request.form)

    if not form.validate():
        return jsonify(success=False, message="Form not valid.")

    #Check if directory already exist.
    _dir = db_session.query(Directory).filter(Directory.user_id == current_user.id).\
        filter(Directory.name == form.name.data).first()
    if _dir:
        return jsonify(success=False, message="Directory already exists.")

    _dir = Directory(name=form.name.data, user_id=current_user.id)
    db_session.add(_dir)
    db_session.commit()

    return jsonify(success=True, message="Directory created.")

@mod.route("/directory/add/feed", methods=["POST"])
@login_required
def add_feed_dir():
    form = AddFeedDirForm(request.form)
    if not form.validate():
        return jsonify(success=False, message="Form not valid.")

    #Check if this user actually owns that directory.
    _dir = db_session.query(Directory).filter(Directory.id == form.dir_id.data).\
        filter(Directory.user_id == current_user.id).first()

    if not _dir:
        return jsonify(success=False, message="Cannot find this directory.")

    de = db_session.query(DirEntry).filter(DirEntry.feed_id == form.feed_id.data).\
        filter(DirEntry.dir_id == form.dir_id.data).first()
    if de:
        return jsonify(success=False, message="This feed is already in this directory.")

    result = db_session.query(UserFeeds).filter(UserFeeds.user_id == current_user.id).\
        filter(UserFeeds.feed_id == form.feed_id.data).first()

    if result:
        db_session.delete(result)

    de = DirEntry(feed_id=form.feed_id.data, dir_id=form.dir_id.data)
    db_session.add(de)
    db_session.commit()

    return jsonify(success=True, message="Feed added to directory.")