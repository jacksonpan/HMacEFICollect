from mongoengine import *


class Sex:
    woman = 0
    man = 1


class User(Document):
    # 用户名
    username = StringField(required=True, unique=True)
    # 密码 md5
    password_md5 = StringField(required=True)
    # 昵称
    nickname = StringField(required=True, default='')
    # 性别
    sex = IntField(required=True, default=Sex.man)
    # 邮箱
    mail = StringField(required=True, default='')
    # 创建时间
    create_time = DateTimeField(required=True)
    # 最后登录时间
    last_login_time = DateTimeField(required=True)
    # 登录授权凭证
    access_token = StringField(required=True)
    # 登录授权过期时间
    access_token_expired_time = DateTimeField(required=False)
    # 是否被删除
    deleted = BooleanField(required=True, default=False)