__author__ = 'DownGoat'


from flask import *
from pyfeedreader.database import db_session
from flask.ext.login import *
import json
from pyfeedreader.models.ReadEntries import ReadEntry
from pyfeedreader.models.entry import Entry


mod = Blueprint('entry', __name__)


@mod.route("/entry", methods=["POST", "GET", "PUT", "DELETE"])
@login_required
def entry():
    if request.method == "GET":
        return get_entry()
    elif request.method == "POST":
        return post_entry()
    elif request.method == "PUT":
        return put_entry()
    elif request.method == "DELETE":
        return delete_entry()

    abort(400)


def get_entry():
    try:
        entry_id = int(request.args.get("id"))
    except (ValueError, TypeError):
        return jsonify(success=False, message="No, or invalid ID value.", link="")

    entry = db_session.query(Entry).filter(Entry.id == entry_id).first()

    if entry:
        return jsonify(success=True, results=Entry.json_entry(entry))
    else:
        return jsonify(success=False, message="No entry with ID {0}.".format(entry_id), link="")


def post_entry():
    abort(400)


def put_entry():
    try:
        data = json.loads(request.data)
    except ValueError:  # Validate JSON
        return jsonify(success=False, message="Bad JSON request.", link="")

    action = data.get("action")
    entry_id = data.get("id")

    # Check that there is a entry ID and action.
    if action is None:
        return jsonify(success=False, message="No Action given.", link="")

    if entry_id is None:
        return jsonify(success=False, message="No entry id given.", link="")

    entry = db_session.query(Entry).filter(Entry.id == entry_id).first()
    if entry is None:
        return jsonify(success=False, message="No entry with that ID.", link="")

    if action == "mark_read":
        read_entries = db_session.query(ReadEntry).filter(ReadEntry.entry_id == current_user.id).all()

        if read_entries:
            return jsonify(success=False, message="Entry already marked as read.", link="")

        db_session.add(ReadEntry(entry_id, current_user.id))
        db_session.commit()

        return jsonify(success=True)

    elif action == "mark_unread":
        read_entries = db_session.query(ReadEntry).filter(ReadEntry.entry_id == current_user.id).all()

        if read_entries is None:
            return jsonify(success=False, message="Already marked as unread.", link="")

        for read_entry in read_entries:
            db_session.delete(read_entry)

        db_session.commit()

        return jsonify(success=True)

    else:
        return jsonify(success=False, message="Unknown action.", link="")


def delete_entry():
    abort(400)