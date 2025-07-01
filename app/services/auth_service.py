from flask import jsonify
from flask_jwt_extended import create_access_token
from typing import Tuple
from flask.wrappers import Response
from app.schemas import LoginRequest


class AuthService:

    @classmethod
    def login(cls, login_request: LoginRequest) -> Tuple[Response, int]:
        if login_request.username != "rbt" or login_request.password != "rbt":
            return jsonify({"msg": "Bad username or password"}), 401

        access_token = create_access_token(identity=login_request.username)
        return jsonify(access_token=access_token), 200