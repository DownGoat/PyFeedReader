__author__ = 'DownGoat'

from flask import *
from pyfeedreader.database import db_session
from flask.ext.login import *
from pyfeedreader.models.category import Category
from pyfeedreader.models.category_entry import CategoryEntry


mod = Blueprint('category', __name__)


@mod.route("/category", methods=["POST", "GET", "PUT", "DELETE"])
@login_required
def category():
    if request.method == "GET":
        return get_category()
    elif request.method == "POST":
        return post_category()
    elif request.method == "PUT":
        return put_category()
    elif request.method == "DELETE":
        return delete_category()

    abort(400)


def get_category():
    categories = db_session.query(Category).filter(Category.user_id == current_user.id).all()

    return jsonify(success=True, results=Category.json_list(categories))


def post_category():
    """
    The POST request creates a Category. Example request format below:
    {
        "name":"Python stuff"
    ]
    :return:
    """
    try:
        data = json.loads(request.data)
    except ValueError:  # Validate JSON
        return jsonify(success=False, message="Bad JSON request.", link="")

    name = data.get("name")

    if not name:
        return jsonify(success=False, message="Bad JSON request.", link="")

    results = db_session.query(Category).filter(Category.name == name, Category.user_id == current_user.id).first()
    if results:
        return jsonify(success=False, message="Category with that name already exists.", link="")

    db_session.add(Category(name, current_user.id))
    db_session.commit()

    return jsonify(success=True)


def put_category():
    abort(400)


def delete_category():
    """
    This request will delete all categories.

    :return:
    """
    categories = db_session.query(Category).filter(Category.user_id == current_user.id).all()

    for category in categories:
        db_session.delete(category)

    db_session.commit()


@mod.route("/category/<int:_id>", methods=["POST", "GET", "PUT", "DELETE"])
@login_required
def category_id(_id):
    if request.method == "GET":
        return get_category_id(_id)
    elif request.method == "POST":
        return post_category_id(_id)
    elif request.method == "PUT":
        return put_category_id(_id)
    elif request.method == "DELETE":
        return delete_category_id(_id)

    abort(400)


def get_category_id(_id):
    """
    Gets the specific Category objects and returns a JSON version of it.

    :param _id: The Category ID.
    :return:
    """
    # Check if the category belongs to the user.
    category = db_session.query(Category).filter(Category.id == _id, Category.user_id == current_user.id).first()

    if not category:
        return jsonify(success=False, message="Unknown ID.", link="")

    category = Category.json(category)
    return jsonify(success=True, results=category)


def post_category_id(_id):
    abort(400)


def put_category_id(_id):
    """
    Update a Category, either add a feed or rename the category.

    :param _id: The Category ID.

    Add new feed example:
    {
        "action": "add",
        "feed_id" 1
    }

    Rename category example:
    {
        "action": "rename",
        "name", "new name"
    }
    :return:
    """
    try:
        data = json.loads(request.data)
    except ValueError:  # Validate JSON
        return jsonify(success=False, message="Bad JSON request.", link="")

    action = data.get("action")

    # Check if the category belongs to the user.
    category = db_session.query(Category).filter(Category.id == _id, Category.user_id == current_user.id).first()

    if not category:
        return jsonify(success=False, message="Unknown ID.", link="")

    # Rename the category action.
    if action == "rename":
        name = data.get("name")
        if not name:  # Need to check if name is set.
            return jsonify(success=False, message="Bad JSON request.", link="")

        category.name = name

    # Add a feed to the category.
    elif action == "add":
        feed_id = data.get("feed_id")
        if not feed_id:
            return jsonify(success=False, message="Bad JSON request.", link="")

        db_session.add(CategoryEntry(feed_id, _id))

    else:
        return jsonify(success=False, message="Unknown action.", link="")

    db_session.commit()

    return jsonify(success=True)


def delete_category_id(_id):
    """
    A delete request can either remove a feed from a category or delete the category altogether.

    :param _id: The Category ID.

    Remove feed request:
    {
        "action": "remove_feed",
        "feed_id": 1
    }

    Delete category reqeust:
    {
        "action": "delete"
    }

    If the category is delete feeds should not be deleted.
    :return:
    """
    try:
        data = json.loads(request.data)
    except ValueError:  # Validate JSON
        return jsonify(success=False, message="Bad JSON request.", link="")

    if data.get("action") is None:
        return jsonify(success=False, message="Bad JSON request.", link="")

    action = data.get("action")

    # Check if the category belongs to the user.
    category = db_session.query(Category).filter(Category.id == _id, Category.user_id == current_user.id).first()

    if not category:
        return jsonify(success=False, message="Unknown ID.", link="")

    # Remove feed from category action
    if action == "remove_feed":
        feed_id = data.get("feed_id")

        if not feed_id:
            return jsonify(success=False, message="Bad JSON request.", link="")

        category_entry = db_session.query(CategoryEntry).filter(
            CategoryEntry.feed_id == feed_id, CategoryEntry.category_id == _id
        ).first()

        db_session.delete(category_entry)

    # Delete the entire category action.
    elif action == "delete":
        category = db_session.query(Category).filter(Category.id == _id).first()
        db_session.delete(category)

    else:
        return jsonify(success=False, message="Unknown action.", link="")

    db_session.commit()

    return jsonify(success=True)
