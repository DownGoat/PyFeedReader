__author__ = 'sis13'

from sqlalchemy import Column, Integer, ForeignKey

from pyfeedreader.database import Model


class UserFeeds(Model):
    __tablename__ = "UserFeeds"
    id = Column('id', Integer, primary_key=True)
    feed_id = Column(Integer)
    user_id = Column(Integer, ForeignKey('user.id'))

    def __init__(self, feed_id, user_id):
        self.feed_id = feed_id
        self.user_id = user_id

    def __repr__(self):
        return '<UserFeeds %r>' % self.username