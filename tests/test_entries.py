import json
from pyfeedreader.models.entry import Entry

__author__ = 'sis13'

import unittest
import pyfeedreader

USERNAME = "downgoat"
PASSWORD = "123qwe"


class EntriesTests(unittest.TestCase):

    def test_entries_get(self):
        self.login(USERNAME, PASSWORD)
        self.add_entry("http://link.com/page1", "http://link.com/page1")

        rv = self.app.get("/entries?limit=1&offset=0")

        print(rv.data)
        assert '"success": true' in rv.data and "http://link.com/page1" in rv.data

    def test_entries_get_none(self):
        self.login(USERNAME, PASSWORD)

        rv = self.app.get("/entries?limit=1&offset=10")

        print(rv.data)
        assert '"results": []' in rv.data

    def test_entries_post(self):
        self.login(USERNAME, PASSWORD)

        rv = self.app.post("/entries")

        assert rv.status_code == 400

    def test_entries_put(self):
        self.login(USERNAME, PASSWORD)
        self.add_entry("http://link.com/page1", "http://link.com/page1")

        rv = self.app.put("/entries", data=json.dumps({"ids": [1]}))
        print(rv.data)

        assert '"success": true' in rv.data

    def test_entries_put_noids(self):
        self.login(USERNAME, PASSWORD)

        rv = self.app.put("/entries", data=json.dumps({"ids": []}))

        print(rv.data)

        assert 'No Entry IDs given, and or invalid JSON.' in rv.data

    def test_entries_put_invalid_json(self):
        self.login(USERNAME, PASSWORD)

        rv = self.app.put("/entries", data='{"ids:[]}')

        print(rv.data)

        assert 'No Entry IDs given, and or invalid JSON.' in rv.data

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
        rv = self.app.post("/createaccount", data={
            "email": "sindre@downgoat.net",
            "username": "downgoat",
            "emailc": "sindre@downgoat.net",
            "password": "123qwe",
            "passwc": "123qwe",
        })


class EntriesFeedIDTests(unittest.TestCase):
    def test_entry_feed_post(self):
        self.login(USERNAME, PASSWORD)
        rv = self.app.post("/entries/1")

        print(rv.data)
        assert rv.status_code == 400

    def test_entry_feed_delete(self):
        self.login(USERNAME, PASSWORD)
        rv = self.app.delete("/entries/1")

        print(rv.data)
        assert rv.status_code == 400

    def test_entry_feed_get(self):
        self.login(USERNAME, PASSWORD)
        self.add_entry("http://link.com/page1", "http://link.com/page1")

        rv = self.app.get("/entries/1")

        print(rv.data)
        assert "http://link.com/page1" in rv.data

    def test_entry_feed_get_none(self):
        self.login(USERNAME, PASSWORD)
        self.add_entry("http://link.com/page1", "http://link.com/page1")

        rv = self.app.get("/entries/2")

        print(rv.data)
        assert '"results": []' in rv.data

    def test_entry_feed_put(self):
        self.login(USERNAME, PASSWORD)
        self.add_entry("http://link.com/page1", "http://link.com/page1")

        assert 1 == 0

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
        rv = self.app.post("/createaccount", data={
            "email": "sindre@downgoat.net",
            "username": "downgoat",
            "emailc": "sindre@downgoat.net",
            "password": "123qwe",
            "passwc": "123qwe",
        })