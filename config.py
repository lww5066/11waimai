class Config():
    # 配置密钥
    SECRET_KEY='laoli'

    # 设置连接数据库的URL
    SQLALCHEMY_DATABASE_URI = 'mysql://root:lw123456@127.0.0.1:3306/1811_flask'

    # 数据库和模型类同步修改
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # 查询时会显示原始SQL语句
    SQLALCHEMY_ECHO = True

    APP_ID = 'wx8ef3c81abf9982d4'
    APP_SECRET = '086e4b04a12e926d254726c4967774b5'

    # 配置静态资源的url 可以动态更换域名 端口号
    STATIC_D='http://127.0.0.1:5000/static/'

    # 图片的路径 静态资源路径
    DOMAIN = 'http://127.0.0.1:5000'
    IGNORE_URLS = ['/api/vi/user/login']

    # 忽略需要验证登陆的接口
    IGNORE_URLES = ['/api/v1/member/login',
                   '/api/v1/member/cklogin',
                   '/api/v1/food/search',
                   '/api/v1/food/all',
                   '/api/v1/food/info']



# 线上环境
class ProductingConfig(Config):
    DEBUG = False


# 生产环境
class DevelopmentConfig(Config):
    DEBUG = True


mapping_config = {
    'pro': ProductingConfig,
    'dev': DevelopmentConfig,
}
