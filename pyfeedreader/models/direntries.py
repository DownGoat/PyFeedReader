from sqlalchemy.orm import relationship

__author__ = 'sis13'

from pyfeedreader.database import Model
from sqlalchemy import Column, Integer, String, Text, ForeignKey


class DirEntry(Model):
    __tablename__ = "DirEntry"
    id = Column('id', Integer, primary_key=True)
    feed_id = Column(Integer)
    dir_id = Column(Integer, ForeignKey('Directory.id'))

    def __repr__(self):
        return '<Directory %r>' % self.username