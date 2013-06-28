__author__ = 'DownGoat'

from pyfeedreader.database import Model
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from pyfeedreader.models.feed import Feed


class Category(Model):
    """
    The Category class represent a category that is a user named collection of feeds.
    """
    __tablename__ = "category"
    id = Column('id', Integer, primary_key=True)
    name = Column(String(128))
    user_id = Column(Integer, ForeignKey('user.id'))
    category_entries = relationship("CategoryEntry")

    def __init__(self, name=None, user_id=None):
        self.name = name
        self.user_id = user_id

    def __repr__(self):
        return '<Category %r>' % self.username

    def get_feeds(self, db_session):
        """
        Creates the class variable feeds which is a list of the feed objects for this category.

        :param session: The current database session.
        :return:
        """
        self.feeds = []
        for entry in self.category_entries:
            f = db_session.query(Feed).filter(Feed.id == entry.feed_id).first()
            if f:
                self.feeds.append(Feed.unread(f, db_session))

    @staticmethod
    def json(category):
        """
        Turns the category into a JSON ready dict.

        :param db_session: The current database session.
        :param curent_user: The User object of the current logged in user.
        :return: Returns a JSON ready dict of the Category object.
        """
        sum = 0

        for feed in category.feeds:
            sum += feed.unread

        return {
            "name": category.name,
            "id": category.id,
            "feeds": Feed.json_list(category.feeds),
            "unread": sum,
        }

    @staticmethod
    def json_list(categories):
        """
        Turns a list on Category objects into a list of JSON ready Category objects.

        :param categories: The list of Category objects you want to make JSON ready.
        :param db_session: The current database session.
        :param current_user: The User object of the currently logged in user.
        :return: Returns a list of JSON ready Category dicts.
        """
        json_ready = []
        for category in categories:
            json_ready.append(
                Category.json(category)
            )

        return json_ready

