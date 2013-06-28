from pyfeedreader.models.entry import Entry

__author__ = 'DownGoat'


import unittest
import pyfeedreader
import json

USERNAME = "downgoat"
PASSWORD = "123qwe"


class CategoryTests(unittest.TestCase):
    def add_entry(self, link, remote_id):
        self.app.post("/feeds", data={
            "feed": "http://someother.com"
        })

        ent = Entry(
            feed_id=1,
            published=1,
            updated=1,
            title="My entry.",
            content="abc"*100,
            description="Some description.",
            link=link,
            remote_id=remote_id,
            unread=True
        )

        self.db_session.add(ent)
        self.db_session.commit()

    def setUp(self):
        self.db_session = pyfeedreader.database.db_session
        self.app = pyfeedreader.app.test_client()
        pyfeedreader.database.init_db()
        self.create_user()

    def tearDown(self):
        self.logout()
        self.db_session.remove()
        pyfeedreader.database.drop_all()

    def login(self, username, password):
        return self.app.post("/login", data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get("/logout", follow_redirects=True)

    def create_user(self):
        rv = self.app.post("/register", data={
            "email": "sindre@downgoat.net",
            "username": "downgoat",
            "emailc": "sindre@downgoat.net",
            "password": "123qwe",
            "passwc": "123qwe",
        })