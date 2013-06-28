__author__ = 'DownGoat'

from sqlalchemy import Column, Integer, ForeignKey
from pyfeedreader.database import Model


class CategoryEntry(Model):
    __tablename__ = "category_entry"
    id = Column('id', Integer, primary_key=True)
    feed_id = Column(Integer)
    category_id = Column(Integer, ForeignKey('category.id'))

    def __init__(self, feed_id=None, category_id=None):
        self.feed_id = feed_id
        self.category_id = category_id

    def __repr__(self):
        return '<CategoryEntry %r>' % self.id