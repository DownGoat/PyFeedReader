__author__ = 'DownGoat'

from pyfeedreader.database import Model
from sqlalchemy import Column, Integer, String, Text, desc
from sqlalchemy.orm import relationship
from pyfeedreader.models.entry import Entry
from pyfeedreader.models.feed import Feed


class User(Model):
    __tablename__ = "user"
    id = Column('id', Integer, primary_key=True)
    email = Column(String(256))
    password = Column(Text)
    current_login = Column(Integer)
    last_login = Column(Integer)
    username = Column(String(100))
    categories = relationship("Category")
    feeds = relationship("UserFeeds")
    category_entries = relationship("UserFeeds")

    def __init__(self, email=None, password=None, current_login=None, last_login=None, username=None,
                 categories=[], feeds=[], read_ents=[]):
        self.email = email
        self.password = password
        self.current_login = current_login
        self.last_login = last_login
        self.username = username
        self.categories = categories
        self.feeds = feeds
        self.read_ents = read_ents

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def q_categories(self, session):
        """
        Dont remember what this function is for
        TODO fix this.
        :param session:
        :return:
        """
        for category in self.categories:
            category.get_feeds(session)

    def get_feeds(self, session):
        temp_list = []
        for uf in self.feeds:
            f = session.query(Feed).filter(Feed.id == uf.feed_id).first()
            if f:
                temp_list.append(f)

        self.rfeed = temp_list

    def feed_entities(self, session):
        ids = []
        for feed in self.feeds:
            ids.append(feed.feed_id)

        for category in self.categories:
            for category_entry in category.category_entries:
                ids.append(category_entry.feed_id)

        self.entries = session.query(Entry).filter(Entry.feed_id.in_(ids)).order_by(desc(Entry.updated)).all()

        for entry in self.entries:
            entry.unread = True
            for read_ent in self.read_ents:
                if entry.id == read_ent.entry_id:
                    entry.unread = False

    def get_entries(self, session, offset, limit):
        self.get_feeds(session)

        ids = []
        for feed in self.feeds:
            ids.append(feed.feed_id)

        query = session.query(Entry).filter(Entry.feed_id.in_(ids)).order_by(desc(Entry.updated)).limit(limit).offset(
            offset)

        return query.all()

    def __repr__(self):
        return '<user %r>' % self.username