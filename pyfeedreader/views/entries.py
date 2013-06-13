from sqlalchemy import desc
from pyfeedreader.models.ReadEntries import ReadEntry
from pyfeedreader.models.entry import Entry

__author__ = 'sis13'

from pyfeedreader.models.userfeeds import UserFeeds
from pyfeedreader.models.feed import Feed
from flask import *
from urlparse import urlparse
from pyfeedreader.database import db_session
from flask.ext.login import *
from pyfeedreader.util import validate_url
import json

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
    limit = request.args.get("limit")
    print(request.form.get("limit"))
    offset = request.args.get("offset")

    if limit is None or offset is None:
        return jsonify(success=False, message="Invalid limit and or offset.")

    entries = current_user.get_entries(db_session, offset, limit)

    return jsonify(success=True, results=Entry.json_list(entries))


def post_entries():
    abort(400)


def put_entries():
    try:
        data = json.loads(request.data)
    except ValueError:
        return jsonify(success=False, message="No Entry IDs given, and or invalid JSON.")

    if len(data["ids"]) is 0:
        return jsonify(success=False, message="No Entry IDs given, and or invalid JSON.")

    for entry_id in data["ids"]:
        db_session.add(ReadEntry(entry_id, current_user.id))

    db_session.commit()

    return jsonify(success=True)


def delete_entries():
    abort(400)
