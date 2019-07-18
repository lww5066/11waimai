from app.libs.redprint import RedPrint
from app import db
from app.models.address import MemberAddress
from flask import jsonify,request,g
api = RedPrint('address',description='地址模块')

# 添加收货地址
@api.route('/set',methods=['POST'])
def set():
    res = {'code':1,'msg':'成功','data':{}}
    # 验证登陆
    member=g.member
    if not member:
        res['code'] = -1
        res['msg'] = '请先登陆'
        return jsonify(res)

    # 接收前端传递数据
    nickname=request.form.get('nickname')
    mobile = request.form.get('mobile')
    province_id = request.form.get('province_id')
    province_str = request.form.get('province_str')
    city_id = request.form.get('city_id')
    city_str = request.form.get('city_str')
    area_id = request.form.get('area_id')
    area_str = request.form.get('area_str')
    address = request.form.get('address')

    if not all([nickname,mobile,province_id,province_str,city_id,city_str,area_id,area_str,address]):
        res['code'] = -1
        res['msg'] = '请填写完整收货地址'
        return jsonify(res)
    # 手机号验证

    # 存入数据库
    memberaddress = MemberAddress()
    memberaddress.nickname = nickname
    memberaddress.mobile = mobile
    memberaddress.province_id = province_id
    memberaddress.province_str = province_str
    memberaddress.city_id = city_id
    memberaddress.city_str = city_str
    memberaddress.area_id = area_id
    memberaddress.area_str = area_str
    memberaddress.address = address
    memberaddress.member_id = member.id

    # 查找数据库中是否存在地址
    count = MemberAddress.query.filter_by(member_id=member.id, is_default=1).count()
    if count == 0:
        memberaddress.is_default = 1
    else:
        memberaddress.is_default = 0

    db.session.add(memberaddress)
    db.session.commit()

    return jsonify(res)

# 收货地址展示
@api.route('/list')
def list():
    res = {'code': 1, 'msg': '成功', 'data': {}}
    # 验证登陆
    member = g.member
    if not member:
        res['code'] = -1
        res['msg'] = '请先登陆'
        return jsonify(res)

    # 从数据库中查找收货地址
    # memberaddresses = MemberAddress.query.filter_by(member_id=member.id).all()
    # addressList=[]
    # for address in memberaddresses:
    #     memberaddres={}
    #     memberaddres['nickname']=address.nickname
    #     memberaddres['mobile'] = address.mobile
    #     memberaddres['province_str'] = address.province_str
    #     memberaddres['city_str'] = address.city_str
    #     memberaddres['area_str'] = address.area_str
    #     memberaddres['address'] = address.address
    #     addressList.append(memberaddres)
    # res['data']['addressList']=addressList

    memberaddresses = MemberAddress.query.filter_by(member_id=member.id).all()
    addressList = []
    for address in memberaddresses:
        temp_addess = {}
        temp_addess['id'] = address.id
        temp_addess['name'] = address.nickname
        temp_addess['mobile'] = address.mobile
        temp_addess['isDefault'] = address.is_default
        temp_addess['detail'] = address.province_str + address.city_str + address.area_str + address.address
        print(temp_addess,'=================================================================================')
        addressList.append(temp_addess)
    res['data']['addressList'] = addressList

    return jsonify(res)



