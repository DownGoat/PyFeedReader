__author__ = 'DownGoat'

from pyfeedreader.models.category import Category
from pyfeedreader.models.category_entry import CategoryEntry
from pyfeedreader.models.userfeeds import UserFeeds
import feedparser
from urlparse import urlparse
from flask import *
from pyfeedreader.database import db_session
from pyfeedreader.config import config
from flask.ext.login import *
from pyfeedreader.models.feed import Feed


mod = Blueprint('feed', __name__)


@mod.route("/feed/new", methods=["POST"])
@login_required
def add_feed():
    """

    :return:
    """
    # TODO This should be JSON too for the sake of consistency.
    feed_url = request.form.get("feed").lower()
    if not feed_url.startswith("https://") and not feed_url.startswith("http://"):
        feed_url = "http://" + feed_url

    feed = db_session.query(Feed).filter(Feed.feed_url == feed_url).first()

    #Dont need new DB entry if it allready is in DB. Update subscribers.
    if feed:
        feed.subscribers += 1
        db_session.query(Feed).filter(Feed.id == feed.id).update({
            "feed_url": feed_url,
            "title": feed.title,
            "last_checked": 1,
            "subscribers": feed.subscribers,
        })

        uf = db_session.query(UserFeeds).filter(user_id=current_user.id, feed_id=feed.id).first()
        if uf:
            return jsonify(success=False, message="Feed already added.")

    else:
        feed = Feed()
        d = feedparser.parse(feed_url, agent=config.get("User-agent"))
        print(d)
        print(feed_url)
        if d.bozo:
            return jsonify(success=False, message="Invalid URL, Bozo error.")

        title = d.feed.get("title", None)

        #Use netloc part of URL if feed has no title element.
        if not title:
            url = urlparse(feed_url)

            #If URL does not have a netloc, something must have gone terrible wrong.
            if url.netloc == "":
                db_session.rollback()
                return jsonify(success=False, message="Invalid URL.")

            title = url.netloc

        feed.title = title
        feed.feed_url = feed_url
        feed.subscribers = 1
        feed.last_checked = 1

        # noinspection PyUnresolvedReferences,PyUnresolvedReferences
        db_session.add(feed)
        db_session.commit()

    #Add the feed as directory entry if a directory is set.
    #If a UserFeed is made aswell the feed will appear twice in the
    #feed column on the mainpage.
    category = request.form.get("directory", None)
    if category:
        _cat = db_session.query(Category).filter(Category.name == category).first()
        if not _cat:
            db_session.rollback()
            return jsonify(success=False, message="Invalid directory.")

        ce = CategoryEntry(_cat=_cat.id, feed_id=feed.id)
        db_session.add(ce)

    #Must make user entry since no directory specified.
    else:
        uf = UserFeeds(feed_id=feed.id, user_id=current_user.id)
        db_session.add(uf)

    db_session.commit()

    return jsonify(success=True, message="Feed Added.")

@mod.route("/feed/delete", methods=["POST"])
@login_required
def delete_feed():
    feed_id = request.form.get("feed", None)
    if not feed_id:
        return jsonify(success=False, message="Invalid form.")

    #Make sure that the current_user is the owner of the feed.
    uf = db_session.query(UserFeeds).filter(UserFeeds.feed_id == feed_id).\
        filter(UserFeeds.user_id == current_user.id).first()
    if uf:
        db_session.remove(uf)
        db_session.commit()

        return jsonify(success=True, message="Feed deleted.")

    #Check DirEntries to see if the feed might be there.
    found = False
    for _dir in current_user.dirs:
        for de in _dir.dir_entries:
            if de.feed_id == feed_id:
                db_session.remove(de)

    if found:
        db_session.commit()

        return jsonify(success=True, message="Feed deleted.")

    return jsonify(success=False, message="Cannot find a feed with that ID.")