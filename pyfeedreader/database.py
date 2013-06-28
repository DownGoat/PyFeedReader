__author__ = 'DownGoat'

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from config import config


engine = create_engine(config.get("db_connector"), convert_unicode=True)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
fs_engine = create_engine(config.get("db_connector"), convert_unicode=True)

fs_db_session = scoped_session(sessionmaker(autocommit=False,
                                            autoflush=False,
                                            bind=fs_engine))

Model = declarative_base()
Model.query = db_session.query_property()


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    from pyfeedreader.models import *

    Model.metadata.create_all(bind=engine)


def drop_all():
    Model.metadata.drop_all(bind=engine)