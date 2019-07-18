from flask import Blueprint
from . import user,member
from . import member,food
from . import cart
from . import address
from . import order

def createBluePrint():
    bp = Blueprint('v1', __name__)
    user.api.register(bp)
    member.api.register(bp)
    # 新建视图-->宏图注册到蓝图！！！！
    food.api.register(bp)
    cart.api.register(bp)
    address.api.register(bp)
    order.api.register(bp)
    return bp
