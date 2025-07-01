from flask import Blueprint
from app.schemas import LoginRequest
from flask_pydantic import validate
from app.services import AuthService

# Blueprint for auth-related routes
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["POST"])
@validate(body=LoginRequest)
def login(body: LoginRequest):
    return AuthService.login(login_request=body)
