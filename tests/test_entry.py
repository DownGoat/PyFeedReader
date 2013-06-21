__author__ = 'DownGoat'

import unittest
import pyfeedreader
import json
from pyfeedreader.models.entry import Entry

USERNAME = "DownGoat"
PASSWORD = "123qwe"


class EntryTests(unittest.TestCase):
    def test_entry_get(self):
        self.login(USERNAME, PASSWORD)
        self.add_entry("http://link.com/page1", "http://link.com/page1")

        rv = self.app.get("/entry?id=1")

        print(rv.data)
        assert "http://link.com/page1" in rv.data

    def test_entry_get_no_id(self):
        self.login(USERNAME, PASSWORD)

        rv = self.app.get("/entry")

        print(rv.data)
        assert '"success": false' in rv.data

    def test_entry_get_char_id(self):
        self.login(USERNAME, PASSWORD)

        rv = self.app.get("/entry?id=a")

        print(rv.data)
        assert '"success": false' in rv.data

    def test_entry_get_negative_id(self):
        self.login(USERNAME, PASSWORD)

        rv = self.app.get("/entry?id=-1")

        print(rv.data)
        assert '"success": false' in rv.data

    def test_entry_put_mark_read(self):
        self.login(USERNAME, PASSWORD)
        self.add_entry("http://link.com/page1", "http://link.com/page1")

        rv = self.app.put("/entry", data=json.dumps({
            "action": "mark_read",
            "id": "1",
        }))

        print(rv.data)
        assert '"success": true' in rv.data

    def test_entry_put_no_action(self):
        self.login(USERNAME, PASSWORD)
        self.add_entry("http://link.com/page1", "http://link.com/page1")

        rv = self.app.put("/entry", data=json.dumps({
            "id": "1",
        }))

        print(rv.data)
        assert '"success": false' in rv.data

    def test_entry_put_no_id(self):
        self.login(USERNAME, PASSWORD)
        self.add_entry("http://link.com/page1", "http://link.com/page1")

        rv = self.app.put("/entry", data=json.dumps({
            "action": "mark_read",
        }))

        print(rv.data)
        assert '"success": false' in rv.data

    def test_entry_put_bad_json(self):
        self.login(USERNAME, PASSWORD)
        self.add_entry("http://link.com/page1", "http://link.com/page1")

        rv = self.app.put("/entry", data='{"action:"mark_read"')

        print(rv.data)
        assert '"success": false' in rv.data

    def test_entry_put_wrong_id(self):
        self.login(USERNAME, PASSWORD)
        self.add_entry("http://link.com/page1", "http://link.com/page1")

        rv = self.app.put("/entry", data=json.dumps({
            "action": "mark_read",
            "id": "42",
        }))

        print(rv.data)
        assert '"success": false' in rv.data

    def test_entry_put_mark_unread(self):
        self.login(USERNAME, PASSWORD)
        self.add_entry("http://link.com/page1", "http://link.com/page1")

        rv = self.app.put("/entry", data=json.dumps({
            "action": "mark_read",
            "id": "1",
        }))
        print(rv.data)
        self.assertIn('"success": true', rv.data)

        rv = self.app.put("/entry", data=json.dumps({
            "action": "mark_unread",
            "id": "1",
        }))
        print(rv.data)
        assert '"success": true' in rv.data

    def test_entry_put_already_unread(self):
        self.login(USERNAME, PASSWORD)
        self.add_entry("http://link.com/page1", "http://link.com/page1")

        rv = self.app.put("/entry", data=json.dumps({
            "action": "mark_unread",
            "id": "1",
        }))

        print(rv.data)
        assert '"success": false' in rv.data

    def test_entry_delete(self):
        self.login(USERNAME, PASSWORD)
        rv = self.app.delete("/entry")

        print(rv.data)
        assert rv.status_code == 400

    def test_entry_post(self):
        self.login(USERNAME, PASSWORD)
        rv = self.app.post("/entry")

        print(rv.data)
        assert rv.status_code == 400

    def add_entry(self, link, remote_id):
        self.app.post("/feeds", data={
            "feed": "http://someother.com"
        })

        ent = Entry(
            feed_id=1,
            published=1,
            updated=1,
            title="My entry.",
            content="abc" * 100,
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