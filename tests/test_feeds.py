__author__ = 'sis13'

import unittest
import pyfeedreader

USERNAME = "downgoat"
PASSWORD = "123qwe"


class FeedsTests(unittest.TestCase):

    def setUp(self):
        self.db_session = pyfeedreader.database.db_session
        self.app = pyfeedreader.app.test_client()
        pyfeedreader.database.init_db()
        self.create_user()

    def tearDown(self):
        self.logout()
        self.db_session.remove()
        pyfeedreader.database.drop_all()

    def test_no_feed(self):
        self.login(USERNAME, PASSWORD)
        rv = self.app.get("/feeds")

        print(rv.data)
        assert "User has no feeds." in rv.data

    def test_add_feed(self):
        self.login(USERNAME, PASSWORD)
        rv = self.app.post("/feeds", data={
            "feed": "http://coolfeed.com"
        })

        print(rv.data)
        assert '"success": true' in rv.data

    def test_feeds(self):
        self.login(USERNAME, PASSWORD)
        rv = self.app.post("/feeds", data={
            "feed": "http://coolfeed.com"
        })

        rv = self.app.get("/feeds")

        print(rv.data)
        assert "coolfeed.com" in rv.data

    def test_feed_already_added(self):
        self.login(USERNAME, PASSWORD)
        self.app.post("/feeds", data={
            "feed": "http://coolfeed.com"
        })

        rv = self.app.post("/feeds", data={
            "feed": "http://coolfeed.com"
        })

        print(rv.data)
        assert "Feed already added." in rv.data

    def test_bad_url(self):
        self.login(USERNAME, PASSWORD)
        rv = self.app.post("/feeds", data={
            "feed": "http://malformed,url"
        })

        print(rv.data)
        assert "Invalid URL." in rv.data

    def test_put(self):
        self.login(USERNAME, PASSWORD)
        rv = self.app.put("/feeds")

        print(rv.data)
        assert rv.status_code == 400

    def test_delete(self):
        self.login(USERNAME, PASSWORD)

        self.app.post("/feeds", data={
            "feed": "http://coolfeed.com"
        })

        self.app.post("/feeds", data={
            "feed": "http://someother.com"
        })

        a = self.app.delete("/feeds")

        rv = self.app.get("/feeds")

        print(rv.data)
        assert "User has no feeds." in rv.data

    def test_feed_id_post(self):
        self.login(USERNAME, PASSWORD)
        rv = self.app.post("/feeds/1", data={
            "feed": "http://coolfeed.com"
        })

        print(rv.data)
        assert rv.status_code == 400

    def test_feed_id_get(self):
        self.login(USERNAME, PASSWORD)

        self.app.post("/feeds", data={
            "feed": "http://coolfeed.com"
        })

        rv = self.app.get("/feeds/1")

        print(rv.data)
        assert "http://coolfeed.com" in rv.data

    def test_feed_id_get_bad(self):
        self.login(USERNAME, PASSWORD)

        rv = self.app.get("/feeds/1")

        print(rv.data)
        assert '"success": false' in rv.data

    def test_feed_id_put(self):
        self.login(USERNAME, PASSWORD)

        self.app.post("/feeds", data={
            "feed": "http://coolfeed.com"
        })

        rv = self.app.put("/feeds/1")

        print(rv.data)
        assert '"success": true' in rv.data

    def test_feed_id_put_bad(self):
        self.login(USERNAME, PASSWORD)

        rv = self.app.put("/feeds/1")

        print(rv.data)
        assert '"success": false' in rv.data

    def test_feed_id_delete(self):
        self.login(USERNAME, PASSWORD)

        self.app.post("/feeds", data={
            "feed": "http://coolfeed.com"
        })

        self.app.delete("/feeds/1")

        rv = self.app.get("/feeds")

        print(rv.data)
        assert "User has no feeds." in rv.data

    def test_feed_id_delete_bad(self):
        self.login(USERNAME, PASSWORD)

        rv = self.app.delete("/feeds/1")

        print(rv.data)
        assert '"success": false' in rv.data

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