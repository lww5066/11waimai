from app.libs.redprint import RedPrint
from app.models.food import Category, Food
from flask import jsonify,request,g
# 添加拼接路径是一个静态方法 用来做url路径拼接用
from app.service.url_service import UrlService
# 工具类中的构造静态资源的绝对路径
from app.utils.common import buildPicUrl
from app.models.member import Member
from app.models.cart import MemberCart
from app.service import memberService
from app import db

api = RedPrint(name='cart', description='购物车')

@api.route('/add',methods=['POST'])
def add():
    res = {'code': 1, 'msg': '成功', 'data': {}}
    try:
        # 验证登陆
        member = g.member
        if not member:
            res['code'] = -1
            res['msg'] = '用户不存在'
            return jsonify(res)

        id = request.form.get('id')  # 食品id
        num = request.form.get('num')
        fromtype = request.form.get('fromtype')
        if not all([id, num]):
            res['code'] = -1
            res['msg'] = '缺少参数'
            return jsonify(res)

        id = int(id)
        num = int(num)
        fromtype = int(fromtype)
        if id <= 0:
            res['code'] = -1
            res['msg'] = 'id错误'
            return jsonify(res)

        # 参数检验
        food = Food.query.get(id)

        if not food:
            res['code'] = -1
            res['msg'] = '商品不存在'
            return jsonify(res)

        if food.status != 1:
            res['code'] = -1
            res['msg'] = '商品已下架'
            return jsonify(res)

        if num > food.stock:
            res['code'] = -1
            res['msg'] = '库存不足'
            return jsonify(res)
        if fromtype == 0:  # 从加入购物车过来
            if num <= 0:
                res['code'] = -1
                res['msg'] = '参数错误'
                return jsonify(res)
        else:  # 从加减号过来
            if num != 1 and num != -1:
                res['code'] = -1
                res['msg'] = '参数错误'
                return jsonify(res)

        # 查自己购物车是否存在这个商品
        membercart = MemberCart.query.filter_by(member_id=member.id, food_id=id).first()
        if not membercart:
            membercart = MemberCart()
            membercart.food_id = id
            membercart.member_id = member.id
            membercart.quantity = num
        else:
            membercart.quantity += num
        db.session.add(membercart)
        db.session.commit()
        # 购物车 若存在，就数量累积，若不存在就创建
        res['msg'] = '添加成功'
        return jsonify(res)


    except Exception as e:
        res['code'] = -1
        res['msg'] = '参数错误'
        return jsonify(res)


# 购物车列表接口
@api.route('/list')
def list():
    res = {'code': 1, 'msg': 'success', 'data': {}}
    # 验证登陆
    member=g.member
    if not member:
        res['code'] = -1
        res['msg'] = '用户不存在'
        return jsonify(res)
    # 1.查看登陆用户购物车
    membercarts=MemberCart.query.filter_by(member_id=member.id).all()
    # 2.根据购物车的商品id 商品表
    list=[]
    totalPrice=0
    for cart in membercarts:
        temp_food={}
        food=Food.query.get(cart.food_id)
        # 查不到或者商品下架
        if not food or food.status!=1:
            continue
        # 购物车商品详情信息
        temp_food['id']=cart.id
        temp_food['food_id'] = cart.food_id
        temp_food['pic_url'] = UrlService.BuildStaticUrl(food.main_image)
        temp_food['name'] = food.name
        temp_food['price'] = str(food.price)
        temp_food['active'] = 'true'
        temp_food['number'] = cart.quantity
        totalPrice+=food.price*cart.quantity
        list.append(temp_food)

    res['data']['list']=list
    res['data']['totalPrice'] = str(totalPrice)
    return jsonify(res)

    # 3.返回数据
    """
    {
                    "id": 1080,
					"food_id":"5",
                    "pic_url": "/images/food.jpg",
                    "name": "小鸡炖蘑菇-1",
                    "price": "85.00",
                    "active": true,
                    "number": 1
                },
                {
                    "id": 1081,
					"food_id":"6",
                    "pic_url": "/images/food.jpg",
                    "name": "小鸡炖蘑菇-2",
                    "price": "85.00",
                    "active": true,
                    "number": 1
                }
    """
import json
@api.route('/delete',methods=['POST'])
def delete():
    res = {'code': 1, 'msg': 'success', 'data': {}}
    """
    前端传递过来的商品id列表ids遍历
    """
    ids=request.form.get('ids')
    ids=json.loads(ids)

    for id in ids:
        membercart=MemberCart.query.get(id)
        db.session.delete(membercart)
        db.session.commit()

    return jsonify(res)

