__author__ = 'sis13'

from pyfeedreader.database import Model
from sqlalchemy import Column, Integer, String, Text


class Entry(Model):
    __tablename__ = "entry"
    id = Column('id', Integer, primary_key=True)
    feed_id = Column(Integer)
    published = Column(Integer)
    updated = Column(Integer)
    title = Column(String(1024))
    content = Column(Text)
    description = Column(String(256))
    link = Column(String(1024))
    remote_id = Column(String(1024))

    def __init__(self, feed_id=None, published=None, updated=None, title=None, content=None, description=None,
                 link=None, remote_id=None, unread=True):
        self.feed_id = feed_id
        self.published = published
        self.updated = updated
        self.title = title
        self.content = content
        self.description = description
        self.link = link
        self.remote_id = remote_id
        self.unread = unread