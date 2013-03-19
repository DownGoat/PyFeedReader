__author__ = 'sis13'

from flask import *
from pyfeedreader.models.user import User
from flask.ext.login import *


class Anonymous(AnonymousUser):
    name = u"Mr. Smith"

app = Flask(__name__)
app.config.from_object('config')

app.secret_key = "secret"

app.jinja_env.globals['static'] = (
    lambda filename: url_for('static', filename=filename))

login_manager = LoginManager()

login_manager.anonymous_user = Anonymous
login_manager.login_view = "/login"


@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))

login_manager.setup_app(app)

@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
    fs_db_session.remove()

@app.before_request
def before_request():
    g.user = current_user


from pyfeedreader.database import db_session, fs_db_session
from pyfeedreader.views import createaccount, login, mainpage

#Register blueprints
app.register_blueprint(createaccount.mod)
app.register_blueprint(login.mod)
app.register_blueprint(mainpage.mod)

if __name__ == '__main__':
    app.run(debug=True)