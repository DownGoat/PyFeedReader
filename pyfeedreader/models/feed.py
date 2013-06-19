__author__ = 'sis13'

from sqlalchemy import Column, Integer, String
from pyfeedreader.database import Model


class Feed(Model):
    __tablename__ = "feed"
    id = Column('id', Integer, primary_key=True)
    feed_url = Column(String(1024))
    last_checked = Column(Integer)
    subscribers = Column(Integer)
    title = Column(String(128))
    update_frequency = Column(Integer)
    favicon = Column(String(1024))
    metadata_update = Column(Integer)

    def __init__(self, update_frequency=1, favicon="", feed_url=None, last_checked=1, subscribers=1,
                 title=u"Some feed", metadata_update=1):
        self.feed_url = feed_url
        self.last_checked = last_checked
        self.subscribers = subscribers
        self.title = title
        self.update_frequency = update_frequency
        self.favicon = favicon
        self.metadata_update = metadata_update

    @staticmethod
    def json_list(feeds):
        """
        Creates a json ready list of feeds that is ready for jsonify.

        :param feeds List of feeds to turn to json.

        :return Returns a list of dicts that is ready to be turned to json.
        """
        json_ready = []
        for feed in feeds:
            json_ready.append(
                Feed.json(feed)
            )

        return json_ready

    @staticmethod
    def json(feed):
        """
        Turns a single feed into a json ready dict.

        :param feed The feed to turn to json ready.
        """
        return {
            "feed_url": feed.feed_url,
            "title": feed.title,
            "favicon": feed.favicon,
            "id": feed.id,
        }
