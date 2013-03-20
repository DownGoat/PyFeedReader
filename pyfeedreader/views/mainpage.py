__author__ = 'sis13'

from flask import *
import bcrypt
import random
import time
from pyfeedreader import app
from pyfeedreader.database import db_session
from pyfeedreader.models.user import User
from flask.ext.login import *
from pyfeedreader.models.entry import Entry
from pyfeedreader.models.feed import Feed

lorem = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam adipiscing, ipsum sit amet pretium ornare,
lectus lacus fringilla est, sit amet tristique dolor augue et leo. Ut scelerisque ipsum eu purus vestibulum
nec fringilla quam dictum. Duis ultricies consequat felis at ultrices. Etiam massa mi, pulvinar vitae
pretium eget, sollicitudin vitae orci. Quisque quis mi turpis. Etiam euismod massa at diam laoreet cursus.
Nulla facilisi. Sed molestie, massa vitae vehicula vulputate, leo orci tincidunt ante, sed euismod arcu sem
sed purus. Proin ut nibh nec arcu ullamcorper euismod nec id magna. Integer sagittis sem eu odio dapibus
suscipit. Fusce ultrices consequat sapien, ac bibendum ligula auctor a. Nunc faucibus tempus consectetur.
Morbi facilisis suscipit scelerisque.
"""
mod = Blueprint('index', __name__)

class Dir():
    def __init__(self, title, feeds):
        self.title = title
        self.feeds = feeds

@mod.route("/", methods=["GET"])
@login_required
def index():
    entries = [Entry(title="Unread entry", content=lorem), Entry(title="Read entry", content=lorem)]
    entries[0].unread = True
    entries[1].unread = False

    dirs = [Dir("News", [Feed(title="BBC"), Feed(title="NRK")])]
    dirs[0].feeds[0].new = True
    dirs[0].feeds[0].new_entries = 5
    return render_template("index.html", entries=entries, dirs=dirs)