from app.libs.redprint import RedPrint
from app.models.food import Category, Food
from flask import jsonify
# 添加拼接路径是一个静态方法 用来做url路径拼接用
from app.service.url_service import UrlService
# 工具类中的构造静态资源的绝对路径
from app.utils.common import buildPicUrl
from app.models.cart import MemberCart
api = RedPrint(name='food', description='食品视图')

"""首页接口"""
"""写完视图记得到__init__注册"""


# banners:
#                 //轮播假数据
#                 [
#                 {
#                     "id": 1,
#                     "pic_url": "/images/food.jpg"
#                 },
#                 {
#                     "id": 2,
#                     "pic_url": "/images/food.jpg"
#                 },
#                 {
#                     "id": 3,
#                     "pic_url": "/images/food.jpg"
#                 }
#             ],
#             categories: [
#                 {id: 0, name: "全部"},
#                 {id: 1, name: "川菜"},
#                 {id: 2, name: "东北菜"},
#             ],
@api.route('/search')
def search():
    resp = {'code': 1, 'msg': 'success', 'data': {}}
    # 查询 limit(3)返回三个
    foods = Food.query.filter_by(status=1).limit(3).all()

    # banner
    banners = []
    for food in foods:
        temp_food = {}
        temp_food['id'] = food.id
        temp_food['pic_url'] = UrlService.BuildStaticUrl(food.main_image)
        banners.append(temp_food)

    # 分类
    categorys = Category.query.filter_by(status=1).all()
    categories = []

    # 假数据 数据库里面没有全部这个分类 创建假数据返回给前端
    categories.append({'id': 0, 'name': '全部'})

    for category in categorys:
        temp_category = {}
        temp_category['id'] = category.id
        temp_category['name'] = category.name
        categories.append(temp_category)

    resp['data']['banners'] = banners
    resp['data']['categories'] = categories
    return jsonify(resp)


# 点击切换菜系视图函数
# 假数据
# goods: [
# 			                {
# 			                    "id": 1,
# 			                    "name": "小鸡炖蘑菇-1",
# 			                    "min_price": "15.00",
# 			                    "price": "15.00",
# 			                    "pic_url": "/images/food.jpg"
# 			                },
# 			                {
# 			                    "id": 2,
# 			                    "name": "小鸡炖蘑菇-1",
# 			                    "min_price": "15.00",
# 			                    "price": "15.00",
# 			                    "pic_url": "/images/food.jpg"
# 			                },
# 			                {
# 			                    "id": 3,
# 			                    "name": "小鸡炖蘑菇-1",
# 			                    "min_price": "15.00",
# 			                    "price": "15.00",
# 			                    "pic_url": "/images/food.jpg"
# 			                },
# 			                {
# 			                    "id": 4,
# 			                    "name": "小鸡炖蘑菇-1",
# 			                    "min_price": "15.00",
# 			                    "price": "15.00",
# 			                    "pic_url": "/images/food.jpg"
# 			                }
#
# 			 ],
from flask import request


@api.route('/all')
def all():
    resp = {'code': 1, 'msg': 'success', 'data': {}}
    # 异常处理 cid可能是不存在的id或者是字符串
    try:
        # 后端取出前端传递的分类id即cid
        # # 后端取出前端传递的页码
        cid = request.args.get('cid')
        page=request.args.get('page')
        # 参数校验
        if not cid:
            cid = '0'
        cid = int(cid)
        if not page:
            page='0'
        page = int(page)
        """
        每页取一个
        """
        # 公式分页公式
        pagesize=1
        offset=(page-1)*pagesize
        goods = []
        # 没有过滤查询 查询所有状态有效的数据
        query = Food.query.filter_by(status=1)
        #  默认查询全部
        if cid == 0:
            foods = query.offset(offset).limit(pagesize).all()
        else:
            foods = query.filter_by(cat_id=cid).offset(offset).limit(pagesize).all()
        # cat_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

        # # 查询所有菜
        # foods = Food.query.filter_by(status=1).all()
        for food in foods:
            click_foods = {}
            click_foods['id'] = food.id
            click_foods['name'] = food.name
            # click_foods['min_price'] = str(food.min_price)
            click_foods['price'] = str(food.price)
            click_foods['pic_url'] = buildPicUrl(food.main_image)
            # click_foods['pic_url'] = 'http://127.0.0.1:5000/static'+food.main_image
            print(click_foods, '=================================')
            goods.append(click_foods)

        resp['data']['goods'] = goods
        # 后端传递给前端用来做终止请求的标识
        # 当前端加载完毕数据后会一直请求 此时需要后端来告诉前端数据请求完毕终止请求
        if len(foods) < pagesize:
            resp['data']['ismore'] = 0
        else:
            resp['data']['ismore'] = 1
        return jsonify(resp)
    except Exception as e:
        resp['code'] = -1
        resp['msg'] = '参数错误'
        return jsonify(resp)

"""点击商品跳转详情页"""
@api.route('/info')
def info():
    resp = {'code': 1, 'msg': 'success', 'data': {}}
    try:
        id=request.args.get('id')
        if not id:
            resp['code']=-1
            resp['mag']='参数不能为空'
            return jsonify(resp)
        id=int(id)

        if id<=0:
            resp['code'] = -1
            resp['mag'] = '参数有误'
            return jsonify(resp)
        """
        // "info": {
            //     "id": 1,
            //     "name": "小鸡炖蘑菇",
            //     "summary": '<p>多色可选的马甲</p><p><img src="http://www.timeface.cn/uploads/times/2015/07/071031_f5Viwp.jpg"/></p><p><br/>相当好吃了</p>',
            //     "total_count": 2,
            //     "comment_count": 2,
            //     "stock": 2,
            //     "price": "80.00",
            //     "main_image": "/images/food.jpg",
            //     "pics": [ '/images/food.jpg','/images/food.jpg' ]
            // },
            // buyNumMax:2,
        
        """
        food=Food.query.get(id)
        info={}
        info['id']=food.id
        info['name'] = food.name
        info['summary'] = food.summary
        info['total_count'] = food.total_count
        info['stock'] = food.stock
        info['price'] = str(food.price)
        info['main_image'] = buildPicUrl(food.main_image)
        info['pics'] = [buildPicUrl(food.main_image),buildPicUrl(food.main_image),buildPicUrl(food.main_image),buildPicUrl(food.main_image),]
        resp['data']['info']=info

        """
        一个商品对应多张图片 图片表 以空间换时间
        食品表    图片表
        1.主图    图1 图二
        """
        return jsonify(resp)
    except Exception as e:
        resp['code'] = -1
        resp['msg'] = '参数错误'
        return jsonify(resp)




