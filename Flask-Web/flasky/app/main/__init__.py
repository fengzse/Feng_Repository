from flask import Blueprint

main = Blueprint('main', __name__)  # 实例化蓝本，但是还没有关联路由等模块

from . import views, errors

from ..models import Permission


@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
