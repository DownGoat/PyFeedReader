__author__ = 'sis13'

from pyfeedreader.database import Model
from sqlalchemy import Column, Integer, String


class Feed(Model):
    __tablename__ = "feed"
    id = Column('id', Integer, primary_key=True)
    feed_url = Column(String(1024))
    last_checked = Column(Integer)
    subscribers = Column(Integer)

    def __init__(self, feed_url=None, last_checked=None, subscribers=None):
        self.feed_url = feed_url
        self.last_checked = last_checked
        self.subscribers = subscribers
