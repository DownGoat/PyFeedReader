from sqlalchemy.orm import relationship
from pyfeedreader.models.feed import Feed

__author__ = 'sis13'

from pyfeedreader.database import Model
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from pyfeedreader.models.direntries import DirEntry


class Directory(Model):
    __tablename__ = "Directory"
    id = Column('id', Integer, primary_key=True)
    name = Column(String(128))
    user_id = Column(Integer, ForeignKey('user.id'))
    dir_entries = relationship("DirEntry")

    def __repr__(self):
        return '<Directory %r>' % self.username

    def get_feeds(self, session):
        self.feeds = []
        for entry in self.dir_entries:
            f = session.query(Feed).get(entry.feed_id)
            if f:
                self.feeds.append(f)