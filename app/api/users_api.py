from flask import Blueprint, request
from flask.json import jsonify

from app import db
from app.models import User


blueprint = Blueprint("users_api", __name__, template_folder="templates")

USER_KEYS_GET = {
    "id", "surname", "name", "age", "position",
    "speciality", "address", "email", "city_from",
}
USER_KEYS_POST = USER_KEYS_GET | {"password"}
USER_KEYS_PUT = USER_KEYS_POST - {"id"}


@blueprint.route("/api/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify({"users": [user.to_dict(only=USER_KEYS_GET) for user in users]})


@blueprint.route("/api/users/<int:user_id>", methods=["GET"])
def get_one_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "Not found"})
    return jsonify({"users": user.to_dict(only=USER_KEYS_GET)})


@blueprint.route("/api/users", methods=["POST"])
def post_users():
    user_json = request.json
    if not user_json or (USER_KEYS_POST - user_json.keys()):
        return jsonify({"error": "Empty request"})
    if User.query.get(user_json["id"]) is not None:
        return jsonify({"error": "Id already exists"})
    if User.get_by_email(user_json["email"]) is not None:
        return jsonify({"error": "This email is already used"})

    user = User(
        id=user_json["id"],
        surname=user_json["surname"],
        name=user_json["name"],
        age=user_json["age"],
        position=user_json["position"],
        speciality=user_json["speciality"],
        address=user_json["address"],
        email=user_json["email"],
        city_from=user_json["city_from"],
    )
    user.set_password(user_json["password"])

    db.session.add(user)
    db.session.commit()
    return jsonify({"success": "OK"})


@blueprint.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_users(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "User with this ID doesn't exists"})

    db.session.delete(user)
    db.session.commit()
    return jsonify({"success": "OK"})


@blueprint.route("/api/users/<int:user_id>", methods=["PUT"])
def edit_users(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "User with this ID doesn't exists"})

    user_json = request.json
    if not user_json or (USER_KEYS_PUT - user_json.keys()):
        return jsonify({"error": "Empty request"})
    
    user.surname = user_json["surname"]
    user.name = user_json["name"]
    user.age = user_json["age"]
    user.position = user_json["position"]
    user.speciality = user_json["speciality"]
    user.address = user_json["address"]
    user.email = user_json["email"]
    user.city_from = user_json["city_from"]
    user.set_password(user_json["password"])

    db.session.commit()
    return jsonify({"success": "OK"})
