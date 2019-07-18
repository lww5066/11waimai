# 购物车的模型类  需要导入 在v1---food下导入
from app import db
from .baseModel import BaseModel

class MemberCart(BaseModel, db.Model):
    __tablename__ = 'member_cart'

    id = db.Column(db.Integer, primary_key=True)
    # 会员
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)# 数量


