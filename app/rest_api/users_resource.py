from flask.json import jsonify
from flask_restful import reqparse, abort, Resource

from app import db
from app.models import User


GET_KEYS = {"id", "surname", "name", "age", "position",
    "speciality", "address", "email", "city_from"}


class UserResource(Resource):

    def get(self, user_id):
        user = User.query.get(user_id)
        self.abort_if_user_not_find(user, user_id)
        return jsonify(user.to_dict(only=GET_KEYS))

    def abort_if_user_not_find(self, user, user_id):
        if user is None:
            abort(404, message=f"User {user_id} not found")

    def delete(self, user_id):
        user = User.query.get(user_id)
        self.abort_if_user_not_find(user, user_id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({"success": "OK"})


parser = reqparse.RequestParser()
parser.add_argument("surname", required=True)
parser.add_argument("name", required=True)
parser.add_argument("age", required=True, type=int)
parser.add_argument("position", required=True)
parser.add_argument("speciality", required=True)
parser.add_argument("address", required=True)
parser.add_argument("email", required=True)
parser.add_argument("city_from", required=True)


class UserListResource(Resource):
    def get(self):
        users = User.query.all()
        return jsonify({"users": [u.to_dict(only=GET_KEYS) for u in users]})

    def post(self):
        args = parser.parse_args()
        user = User(
            surname=args["surname"],
            name=args["name"],
            age=args["age"],
            position=args["position"],
            speciality=args["speciality"],
            address=args["address"],
            email=args["email"],
            city_from=args["city_from"],
        )
        db.session.add(user)
        db.session.commit()
        return jsonify({"success": "OK"})
