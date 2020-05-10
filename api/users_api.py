from flask import Blueprint, jsonify, make_response, abort, request
from sqlalchemy.exc import StatementError

from data import db_session
from data.users import User

users_api = Blueprint('users_api', __name__, template_folder='templates')


# users_api добавляется по url_prefix=/api, мне, кажется, так логичней


@users_api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@users_api.route("/users")
def get_users():
    session = db_session.create_session()
    users = session.query(User).all()
    return jsonify({
        "users": [user.to_dict((
                    "surname",
                    "name",
                    "age",
                    "position",
                    "speciality",
                    "address",
                    "email",
                    "city_from"
                )) for user in users]
    })


@users_api.route("/users/<int:user_id>")
def get_user(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404)
    return jsonify({
        "users": user.to_dict((
                    "surname",
                    "name",
                    "age",
                    "position",
                    "speciality",
                    "address",
                    "email",
                    "city_from"
                ))
    })


@users_api.route("/users", methods=["POST"])
def add_user():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ["surname", "name", "age", "email", "password"]):
        return jsonify({'error': 'Bad request'})
    form = request.json
    session = db_session.create_session()
    if session.query(User).get(form.get("id")):
        return jsonify({"error": "Id already exists"})
    elif session.query(User).filter(User.email == form["email"]).first():
        return jsonify({'error': 'Email already exists'})
    all_fields = {"id", "surname", "name", "age", "position", "speciality", "address", "email"}
    kwargs = {field: form[field] for field in all_fields.intersection(set(form))}
    try:
        user = User(**kwargs)
        user.set_password(form["password"])
    except StatementError:
        return jsonify({"error": "Bad request"})
    session.add(user)
    session.commit()
    return jsonify({'success': 'OK'})


@users_api.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404)
    session.delete(user)
    session.commit()
    return jsonify({'success': 'OK'})


@users_api.route("/users/<int:user_id>", methods=["PUT"])
def edit_user(user_id):
    session = db_session.create_session()
    user: User = session.query(User).get(user_id)
    if not user:
        abort(404)
    all_fields = {"surname", "name", "age", "position", "speciality", "address", "email"}
    for field in all_fields.intersection(set(request.json)):
        user.__setattr__(field, request.json[field])
    if request.json.get("password"):
        user.set_password(request.json["password"])
    session.commit()
    return jsonify({"success": "OK"})
