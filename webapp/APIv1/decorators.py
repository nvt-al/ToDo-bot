from functools import wraps

from flask import abort, current_app, request
from flask_login import config, current_user


def login_required_API(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if request.method in config.EXEMPT_METHODS:
            return func(*args, **kwargs)
        elif current_app.config.get("LOGIN_DISABLED"):
            return func(*args, **kwargs)
        elif not current_user.is_authenticated:
            return abort(401)
        return func(*args, **kwargs)

    return decorated_view
