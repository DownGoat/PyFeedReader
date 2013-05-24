__author__ = 'sis13'

from pyfeedreader.models.userfeeds import UserFeeds
from pyfeedreader.models.feed import Feed
from flask import *
from urlparse import urlparse
from pyfeedreader.database import db_session
from flask.ext.login import *
from pyfeedreader.util import validate_url


mod = Blueprint('feeds', __name__)


@mod.route("/feeds", methods=["POST", "GET", "PUT", "DELETE"])
@login_required
def feeds():
    if request.method == "GET":
        return get_feeds()
    elif request.method == "POST":
        return post_feeds()
    elif request.method == "PUT":
        return put_feeds()
    elif request.method == "DELETE":
        return delete_feeds()

    abort(400)


def get_feeds():
    json_feeds = Feed.json_list(current_user.rfeed)

    if not json_feeds:
        return jsonify(success=False, message="User has no feeds.", link="nolink")
    else:
        return jsonify(success=True, results=json_feeds)


def post_feeds():
    if not request.form.get("feed"):
        return jsonify(success=False, message="Invalid request.", link="nolink")

    feed_url = request.form.get("feed").lower()
    if not feed_url.startswith("https://") and not feed_url.startswith("http://"):
        feed_url = "http://" + feed_url

    feed = db_session.query(Feed).filter(Feed.feed_url == feed_url).first()

    if feed:
        uf = db_session.query(UserFeeds).filter(UserFeeds.user_id == current_user.id,
                                                UserFeeds.feed_id == feed.id).first()
        if uf:
            return jsonify(success=False, message="Feed already added.", link="nolink")

        db_session.query(Feed).filter(Feed.id == feed.id).update({
            "subscribers": feed.subscribers + 1,
        })

        uf = UserFeeds(feed.id, current_user.id)
        db_session.add(uf)
        db_session.commit()

        return jsonify(success=True)

    else:
        try:
            validate_url(feed_url)
        except ValueError:
            return jsonify(success=False, message="Invalid URL.", link="nolink")

        url = urlparse(feed_url)
        feed = Feed(feed_url=feed_url, favicon=url.netloc + "/favicon.ico")
        db_session.add(feed)
        db_session.commit()

        uf = UserFeeds(feed.id, current_user.id)
        db_session.add(uf)
        db_session.commit()

        return jsonify(success=True)


def put_feeds():
    abort(400)


def delete_feeds():
    for uf in current_user.feeds:
        try:
            db_session.delete(uf)
        except Exception as e:
            print(e)
        db_session.flush()

    db_session.commit()

    return jsonify(success=True)


@mod.route("/feeds/<int:feed_id>", methods=["POST", "GET", "PUT", "DELETE"])
@login_required
def feeds_id(feed_id):
    if request.method == "GET":
        return get_feeds_id(feed_id)
    elif request.method == "POST":
        return post_feeds_id(feed_id)
    elif request.method == "PUT":
        return put_feeds_id(feed_id)
    elif request.method == "DELETE":
        return delete_feeds_id(feed_id)


def get_feeds_id(feed_id):
    pass


def post_feeds_id(feed_id):
    pass


def put_feeds_id(feed_id):
    pass


def delete_feeds_id(feed_id):
    pass