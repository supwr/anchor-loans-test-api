import functools
from flask import abort, current_app as app
from main.service.users_service import UsersService
from flask_jwt_extended import get_jwt_identity


def admin_required(view):
    @functools.wraps(view)
    def decorated_function(*args, **kwargs):
        current_user = UsersService.get_user_by_username(get_jwt_identity())
        if 'role' not in current_user or current_user["role"] != app.config['ADMIN_ROLE']:
            abort(403)
        return view(*args, **kwargs)
    return decorated_function