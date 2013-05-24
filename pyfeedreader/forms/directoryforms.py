__author__ = 'sis13'

from wtforms import Form, TextField, validators, IntegerField


class NewDirForm(Form):
    name = TextField("name", [
        validators.Required("You must enter a name."),
    ])


class AddFeedDirForm(Form):
    feed_id = IntegerField("feed_id", [
        validators.Required("You must select a feed."),
        ])

    dir_id = IntegerField("dir_id", [
            validators.Required("You must select a directory."),
        ])