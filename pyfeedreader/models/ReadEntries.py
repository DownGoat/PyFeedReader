from sqlalchemy.orm import relationship

__author__ = 'sis13'

from pyfeedreader.database import Model
from sqlalchemy import Column, Integer, String, Text, ForeignKey


class ReadEntry(Model):
    __tablename__ = "ReadEntry"
    id = Column('id', Integer, primary_key=True)
    entry_id = Column(Integer)
    user_id = Column(Integer, ForeignKey('user.id'))


    def __repr__(self):
        return '<ReadEntry %r>' % self.username