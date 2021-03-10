from flask import make_response
from flask.json import jsonify

from app import app


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)
