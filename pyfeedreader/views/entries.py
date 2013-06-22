__author__ = 'DownGoat'

from flask import *
from pyfeedreader.database import db_session
from flask.ext.login import *
import json
from sqlalchemy import desc
from pyfeedreader.models.ReadEntries import ReadEntry
from pyfeedreader.models.entry import Entry

mod = Blueprint('entries', __name__)


@mod.route("/entries", methods=["POST", "GET", "PUT", "DELETE"])
@login_required
def entries():
    if request.method == "GET":
        return get_entries()
    elif request.method == "POST":
        return post_entries()
    elif request.method == "PUT":
        return put_entries()
    elif request.method == "DELETE":
        return delete_entries()

    abort(400)


def get_entries():
    """
    A GET request should return all the entries for the logged in user in. There should be a limit and offset, returning
    all entries is too much data.
    :return:
    """
    try:
        limit = int(request.args.get("limit"))
        offset = int(request.args.get("offset"))
    except (ValueError, TypeError):
        return jsonify(success=False, message="Invalid limit and or offset.")

    if limit is None or offset is None:
        return jsonify(success=False, message="Invalid limit and or offset.")

    if limit < 0 or offset < 0:
        return jsonify(success=False, message="Invalid limit and or offset.")

    if limit > 200:
        return jsonify(success=False, message="Too big range.")

    #Request needs a limit and offset, cannot return all data it is too much.
    if limit is None or offset is None:
        return jsonify(success=False, message="Invalid limit and or offset.")

    entries = current_user.get_entries(db_session, offset, limit)

    return jsonify(success=True, results=Entry.json_list(entries, db_session, current_user.id))


def post_entries():
    abort(400)


def put_entries():
    """
    A PUT request should bulk update a list of entries, the only update that can be done for entries is marking them as
    read.
    :return:
    """
    try:
        data = json.loads(request.data)
    except ValueError:  # Validate JSON.
        return jsonify(success=False, message="No Entry IDs given, and or invalid JSON.")

    #There needs to be at least one ID.
    if len(data["ids"]) is 0:
        return jsonify(success=False, message="No Entry IDs given, and or invalid JSON.")

    for entry_id in data["ids"]:
        db_session.add(ReadEntry(entry_id, current_user.id))

    db_session.commit()

    return jsonify(success=True)


def delete_entries():
    abort(400)


@mod.route("/entries/<int:feed_id>", methods=["POST", "GET", "PUT", "DELETE"])
@login_required
def entries_feed_id(feed_id):
    if request.method == "GET":
        return get_entries_feed(feed_id)
    elif request.method == "POST":
        return post_entries_feed()
    elif request.method == "PUT":
        return put_entries_feed(feed_id)
    elif request.method == "DELETE":
        return delete_entries_feed()

    abort(400)


def post_entries_feed():
    abort(400)


def delete_entries_feed():
    abort(400)


def get_entries_feed(feed_id):
    """
    A GET request should return all entries for that feed, this request will have a limit and offset.

    :param feed_id: The ID of the feed.
    :return:
    """
    try:
        limit = int(request.args.get("limit"))
        offset = int(request.args.get("offset"))
    except (ValueError, TypeError):
        return jsonify(success=False, message="Invalid limit and or offset.")

    if limit is None or offset is None:
        return jsonify(success=False, message="Invalid limit and or offset.")

    if limit < 0 or offset < 0:
        return jsonify(success=False, message="Invalid limit and or offset.")

    if limit > 200:
        return jsonify(success=False, message="Too big range.")

    query = db_session.query(Entry).filter(Entry.feed_id == feed_id).order_by(desc(Entry.updated)).limit(limit).offset(
        offset)

    return jsonify(success=True, results=Entry.json_list(query.all(), db_session, current_user.id))


def put_entries_feed(feed_id):
    """
    A PUT request should bulk update entries for this feed and mark them read or unread.
    The request should include JSON data to specify which kind of update, below is a example
    of a mark read request.
    {
        "action":"mark_read"
    }

    TODO implement mark all unread.

    :return:
    """
    try:
        data = json.loads(request.data)
    except ValueError:  # Validate JSON.
        return jsonify(success=False, message="Invalid JSON.")

    action = data.get("action")

    if not action:
        return jsonify(success=False, message="No action given, need a action.", link="")

    if action == "mark_all_read":
        entries = db_session.query(Entry.id).filter(Entry.feed_id == feed_id).all()

        for entry in entries:
            db_session.add(ReadEntry(entry[0], current_user.id))

        db_session.commit()

        return jsonify(success=True)

    return jsonify(success=False, message="Unkown action.", link="")

