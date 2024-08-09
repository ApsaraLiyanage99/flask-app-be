from flask import Blueprint, request, g
from app.core.middleware import authenticator
from app.core.database import AsyncDBHandler
from app.services.user_service import UserService

user_bp = Blueprint('user', __name__, url_prefix='/user')

db_handler = AsyncDBHandler()


@user_bp.route('/register', methods=['POST'])
async def register():
    data = request.get_json()
    response, status = await UserService.register_user(data, db_handler)
    return response, status


@user_bp.route('/login', methods=['POST'])
async def login():
    data = request.get_json()
    response, status = await UserService.login_user(data, db_handler)
    return response, status


@user_bp.route('/token/refresh', methods=['POST'])
# @authenticator(refresh_token=True)
async def refresh_token():
    refresh_token = request.json.get("refresh_token")
    response, status = await UserService.refresh_token(refresh_token, db_handler)
    return response, status


@user_bp.route('/logout', methods=['POST'])
@authenticator()
async def logout():
    refresh_token = request.json.get("refresh_token")
    response, status = await UserService.logout(refresh_token, db_handler)
    return response, status
