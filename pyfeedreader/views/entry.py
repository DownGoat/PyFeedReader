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
    """
    The GET request should return the entry.
    Below is a example of a GET request:
        /entry?id=1

    :return:
    """
    try:
        entry_id = int(request.args.get("id"))
    except (ValueError, TypeError):
        return jsonify(success=False, message="No, or invalid ID value.", link="")

    entry = db_session.query(Entry).filter(Entry.id == entry_id).first()

    if entry:
        return jsonify(success=True, results=Entry.json_entry(entry, db_session, current_user.id))
    else:
        return jsonify(success=False, message="No entry with ID {0}.".format(entry_id), link="")


def post_entry():
    abort(400)


def put_entry():
    """
    The PUT request should update the entry, it can either be marked as read or marked as unread.
    What kind of update the request is should be specified in the action variable of the JSON data in the request.
    A example of a mark read request is shown below:
    {
        "action":"mark_read",
        "id":"1"
    }

    Action is the type of update that should be done to the entry.
    ID is the ID of the entry to preform the update on.

    Below is a example of a mark unread request:
    {
        "action":"mark_unread",
        "id":"1"
    }

    :return:
    """
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

    # Handling a mark read request.
    if action == "mark_read":
        read_entries = db_session.query(ReadEntry).filter(ReadEntry.entry_id == current_user.id).all()

        if read_entries:
            return jsonify(success=False, message="Entry already marked as read.", link="")

        db_session.add(ReadEntry(entry_id, current_user.id))
        db_session.commit()

        return jsonify(success=True)

    # Handling a mark unread request.
    elif action == "mark_unread":
        #Just in case there are several read entries for the entry remove them all.
        read_entries = db_session.query(ReadEntry).filter(ReadEntry.entry_id == current_user.id).all()

        if len(read_entries) == 0:
            return jsonify(success=False, message="Already marked as unread.", link="")

        for read_entry in read_entries:
            db_session.delete(read_entry)

        db_session.commit()

        return jsonify(success=True)

    else:
        return jsonify(success=False, message="Unknown action.", link="")


def delete_entry():
    abort(400)