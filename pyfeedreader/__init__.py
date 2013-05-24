__author__ = 'sis13'

from flask import *
from pyfeedreader.models.user import User
from flask.ext.login import *
from pyfeedreader.config import config
from pyfeedreader.database import fs_db_session


class Anonymous(AnonymousUser):
    name = u"Mr. Smith"

app = Flask(__name__)
app.config.from_object('pyfeedreader.config')

app.secret_key = "secret"

app.jinja_env.globals['static'] = (
    lambda filename: url_for('static', filename=filename))

login_manager = LoginManager()

login_manager.anonymous_user = Anonymous
login_manager.login_view = "/login"


@login_manager.user_loader
def load_user(userid):
    u = User.query.get(int(userid))
    u.q_dirs(fs_db_session)
    u.get_feeds(fs_db_session)
    return u

login_manager.setup_app(app)

@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
    fs_db_session.remove()

@app.before_request
def before_request():
    g.user = current_user


from pyfeedreader.database import db_session, fs_db_session
from pyfeedreader.views import createaccount, login, mainpage, directory, read, feed, feeds

#Register blueprints
app.register_blueprint(createaccount.mod)
app.register_blueprint(login.mod)
app.register_blueprint(mainpage.mod)
app.register_blueprint(directory.mod)
app.register_blueprint(read.mod)
app.register_blueprint(feed.mod)
app.register_blueprint(feeds.mod)

if __name__ == '__main__':
    app.run(debug=True)