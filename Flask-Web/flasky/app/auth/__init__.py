from flask import Blueprint

auth = Blueprint('auth', __name__)  # 和app实例不同，蓝本实例在本包中就被创建了，其他模块都是引用实例

from . import views
