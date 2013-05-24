from pyfeedreader.models.ReadEntries import ReadEntry

__author__ = 'sis13'

from flask import *

from pyfeedreader.database import db_session
from flask.ext.login import *


mod = Blueprint('read', __name__)

@mod.route("/read", methods=["POST"])
@login_required
def read_entry():
    if not request.form.get("entry_id", None):
        return jsonify(success=False)

    entry_id = request.form.get("entry_id", None)

    read_entry = ReadEntry(entry_id=entry_id, user_id=current_user.id)
    db_session.add(read_entry)
    db_session.commit()

    return jsonify(success=True)