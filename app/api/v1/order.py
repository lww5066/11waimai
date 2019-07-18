from app.libs.redprint import RedPrint
from flask import request, jsonify, g
import json
from app.models.cart import MemberCart
from app.models.food import Food
from app.models.address import MemberAddress
from app.utils.common import buildPicUrl
from app.models.order import PayOrder, PayOrderItem
from app import db
import hashlib, random, time

api = RedPrint(name='order', description='购物车')


@api.route('/commit', methods=['POST'])
def commit():
    res = {'code': 1, 'msg': 'success', 'data': {}}
    # 接受前端传递的ids
    ids = request.form.get('ids')
    ids = json.loads(ids)  # 转成列表

    if not ids:
        res['code'] = -1
        res['msg'] = '参数不全'
        return jsonify(res)

    # 验证登陆
    member = g.member
    if not member:
        res['code'] = -1
        res['msg'] = '请先登陆'
        return jsonify(res)

    goods_list = []  # 商品
    yun_price = 0  # 运费
    pay_price = 0  # 商品金额

    for id in ids:
        temp_data = {}
        # pycharm大写改小写ctrl+shift+u
        membercart = MemberCart.query.filter_by(member_id=member.id, food_id=id).first()
        food = Food.query.get(id)

        temp_data['id'] = id
        temp_data['name'] = food.name
        temp_data['price'] = str(food.price)
        temp_data['pic_url'] = buildPicUrl(food.main_image)
        temp_data['number'] = membercart.quantity
        goods_list.append(temp_data)
        pay_price += food.price * membercart.quantity
    # 查询会员的默认地址
    # 查询条件有两个 1.当前会员的id 数据库中相对应的默认地址isdefault=1
    memberaddress = MemberAddress.query.filter_by(member_id=member.id, is_default=1).first()

    default_address = {}

    # ctrl+D复制当前行到下一行
    default_address['id'] = memberaddress.id
    default_address['nickname'] = memberaddress.nickname
    default_address['mobile'] = memberaddress.mobile
    default_address['address'] = memberaddress.showAddress()
    # 总价
    total_price = yun_price + pay_price
    # 数据返回
    res['data']['goods_list'] = goods_list
    res['data']['default_address'] = default_address
    res['data']['yun_price'] = str(yun_price)
    res['data']['pay_price'] = str(pay_price)
    res['data']['total_price'] = str(total_price)
    return jsonify(res)


# 生成订单
@api.route('/create', methods=['POST'])
def create():
    res = {'code': 1, 'msg': '成功', 'data': {}}
    try:
        member = g.member
        if not member:
            res['code'] = -1
            res['msg'] = '该用户不存在'
            return jsonify(res)

        ids = request.form.get('ids')
        address_id = request.form.get('address_id')
        note = request.form.get('note')

        pay_price = 0
        yun_price = 0
        ids = json.loads(ids)
        # 根据ids查购物车
        for id in ids:
            membercart = MemberCart.query.filter_by(member_id=member.id, food_id=id).first()
            if not membercart:
                continue

            food = Food.query.get(id)

            if not food or food.status != 1:
                continue

            pay_price += food.price * membercart.quantity

        memberaddress = MemberAddress.query.get(address_id)

        if not memberaddress:
            res['code'] = -1
            res['msg'] = '地址不存在'
            return jsonify(res)

        #  1生成订单
        payorder = PayOrder()
        payorder.order_sn = geneOrderSn()  # 唯一
        payorder.total_price = yun_price + pay_price
        payorder.yun_price = yun_price
        payorder.pay_price = pay_price
        payorder.note = note
        payorder.status = -8  # 待付款
        payorder.express_status = -1  # 待发货
        payorder.express_address_id = address_id
        payorder.express_info = memberaddress.showAddress()
        payorder.comment_status = -1  # 待评论
        payorder.member_id = member.id

        db.session.add(payorder)

        # 2扣库存
        foods = db.session.query(Food).filter(Food.id.in_(ids)).with_for_update().all()
        temp_stock = {}  # 临时库存

        for food in foods:
            temp_stock[food.id] = food.stock

        for id in ids:
            membercart = MemberCart.query.filter_by(member_id=member.id, food_id=id).first()

            if membercart.quantity > temp_stock[id]:
                res['code'] = -1
                res['msg'] = '库存不足'
                return jsonify(res)
            # 更新库存
            food = db.session.query(Food).filter(Food.id == id).update({
                'stock': temp_stock[id] - membercart.quantity
            })
            if not food:
                raise Exception('更新失败')

            food = Food.query.get(id)

            # 3 生成订单的商品从表
            payorderitem = PayOrderItem()
            payorderitem.quantity = membercart.quantity
            payorderitem.price = food.price
            payorderitem.note = note
            payorderitem.status = 1
            payorderitem.pay_order_id = payorder.id
            payorderitem.member_id = member.id
            payorderitem.food_id = id

            db.session.add(payorderitem)

            # 4清空购物车
            db.session.delete(membercart)  # 删除下蛋购物车

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        res['code'] = -1
        res['msg'] = '出现异常'
        return jsonify(res)

    return jsonify(res)


def geneOrderSn():
    m = hashlib.md5()
    sn = None
    while True:
        str = "%s-%s" % (int(round(time.time() * 1000)), random.randint(0, 9999999))
        m.update(str.encode("utf-8"))
        sn = m.hexdigest()
        if not PayOrder.query.filter_by(order_sn=sn).first():
            break
    return sn


@api.route('/list')
def list():
    res = {'code': 1, 'msg': '成功', 'data': {}}
    # 验证登陆
    member = g.member
    if not member:
        res['code'] = -1
        res['msg'] = '用户不存在'
        return jsonify(res)
    # status=request.args.get('status')
    # print(status,'=========================================================')
    # if str(status)=='-8':
    #     pass
    # if str(status)=='-7':
    #     pass
    # if str(status)=='-5':
    #     pass
    # if str(status)=='-1':
    #     pass
    # if str(status)=='-0':
    #     pass

    order_list=[]
    # 查询该用户名下的所有订单消息
    payorders=PayOrder.query.filter_by(member_id=member.id).all()
    for payorder in payorders:
        temp_data={}
        temp_data['status']=payorder.status
        temp_data['status_desc']=payorder.status_desc
        temp_data['date']=payorder.create_time.strftime('%Y-%m-%d %H:%M:%S')
        temp_data['note']=payorder.note
        temp_data['total_price']=str(payorder.total_price)
        temp_data['order_number']=payorder.create_time.strftime('%Y-%m-%d %H:%M:%S')+str(payorder.id).zfill(5)
        goods_list=[]
        # 查看订单商品
        payorderitems=PayOrderItem.query.filter_by(pay_order_id=payorder.id).all()
        for payorderitem in payorderitems:
            food=Food.query.get(payorderitem.food_id)
            temp_food={}
            temp_food['pic_url']=buildPicUrl(food.main_image)

            goods_list.append(temp_food)
        temp_data['goods_list']=goods_list
        order_list.append(temp_data)

    res['data']['order_list']=order_list
    return jsonify(res)
