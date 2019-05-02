from flask import Blueprint, render_template, jsonify, request, abort
import json
from bson import json_util
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt
from main.service.users_service import UsersService

users = Blueprint('users', __name__)


@users.route('/register', methods=['POST'])
def new():

    try:
        new_user = request.json

        if new_user["password"] is None or new_user["username"] is None or new_user["fullname"] is None:
            response = jsonify({"message": "Certifique-se que todos os dados foram preenchidos."})
            response.status_code = 400
            return response

        user = UsersService.get_user_by_email_and_username(new_user["username"], new_user["email"])

        if user:
            response = jsonify({"message": "Já existe usuário com esse email/username."})
            response.status_code = 400
            return response

        new_user["password"] = UsersService.generate_hash(new_user['password'])
        user_id = UsersService.new_user(new_user)

        user = UsersService.get_user_by_id(user_id, {"password": 0})
        access_token = create_access_token(identity=new_user['username'], expires_delta=False)

        response = {
            "data": {
                "access_token": access_token,
                "user": user
            }
        }

        return json.dumps(response, default=json_util.default), 200, {'Content-Type': 'application/json; charset=utf-8'}

    except Exception:
        abort(500)


@users.route('/login', methods=['POST'])
def login():

    try:
        login_user = request.json

        if login_user["password"] is None or login_user["username"] is None:
            response = jsonify({"message": "Certifique-se que todos os dados foram preenchidos."})
            response.status_code = 400
            return response

        user = UsersService.get_user_by_username(login_user["username"])

        if not user:
            response = jsonify({"message": "Usuário não encontrado."})
            response.status_code = 400
            return response

        if UsersService.verify_hash(login_user["password"], user["password"]):
            access_token = create_access_token(identity=login_user['username'], expires_delta=False)

            del user["password"]

            response = {
                "data": {
                    "access_token": access_token,
                    "user": user
                }
            }

            return json.dumps(response, default=json_util.default), 200, {
                'Content-Type': 'application/json; charset=utf-8'}

        response = jsonify({"message": "Acesso negado."})
        response.status_code = 403
        return response

    except Exception:
        abort(500)
