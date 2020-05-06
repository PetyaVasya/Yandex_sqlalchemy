from flask import jsonify
from flask_restful import abort, Resource
from sqlalchemy.exc import StatementError

from api_v2.user_parser import parser
from data import db_session
from data.users import User


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


class UsersResource(Resource):

    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({
            "users": user.to_dict((
                "surname",
                "name",
                "age",
                "position",
                "speciality",
                "address",
                "email"
            ))
        })

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class UserListResource(Resource):

    def get(self):
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
                "email"
            )) for user in users]
        })

    def post(self):
        form = parser.parse_args()
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
