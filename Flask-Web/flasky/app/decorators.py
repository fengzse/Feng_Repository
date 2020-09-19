from functools import wraps
from .models import Permission
from flask_login import current_user
from flask import abort


# 在视图函数中检查用户是否具有相关权限
def permission_required(permission):
    def decorator(func):
        @wraps(func)
        def deco_functions(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return func(*args, **kwargs)

        return deco_functions

    return decorator


def admin_required(func):
    return permission_required(Permission.ADMIN)(func)
