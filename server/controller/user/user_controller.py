import uuid
from datetime import datetime

from bson import ObjectId

from controller.basic import HttpCode
from controller.basic.basic_controller import BasicController
from controller.basic.parameters import parameters, check
from libs.codec import _md5
from models.User import User


class UserController(BasicController):

    @parameters(
        username=check(type=str, null=False),
        password_md5=check(type=str, null=False)
    )
    def login(self):
        username = self.parameters.get('username')
        password_md5 = self.parameters.get('password_md5')

        user = User.objects(username=username, password_md5=password_md5, deleted=False).first()
        if not user:
            return self.response_fail(HttpCode.fail, '用户名或密码不正确，请重新输入！')
        user.access_token = _md5(str(uuid.uuid1()))
        user.last_login_time = datetime.now()
        user.save()
        ret = self.process_mongo_to_python(user, pop_keys=['password_md5', 'deleted'])
        return self.response_success(ret)

    @parameters(
        username=check(type=str, null=False),
        password_md5=check(type=str, null=False),
        mail=check(type=str, null=True)
    )
    def create(self):
        username = self.parameters.get('username')
        password_md5 = self.parameters.get('password_md5')
        mail = self.parameters.get('mail')

        user = User.objects(username=username).first()
        if user:
            return self.response_fail(HttpCode.fail, '用户名已存在，请换一个再创建')
        user = User()
        user.username = username
        user.password_md5 = password_md5
        user.mail = mail
        user.create_time = datetime.now()
        user.access_token = _md5(str(uuid.uuid1()))
        user.last_login_time = user.create_time
        user.save()
        ret = self.process_mongo_to_python(user, pop_keys=['password_md5', 'deleted'])
        return self.response_success(ret)

    @parameters(
        user_id=check(type=str, null=False),
        access_token=check(type=str, null=False),
        old_password_md5=check(type=str, null=True),
        new_password_md5=check(type=str, null=True),
        nickname=check(type=str, null=True),
        sex=check(type=str, null=True),
        mail=check(type=str, null=True),
    )
    def update(self):
        user_id = self.parameters.get('user_id')
        access_token = self.parameters.get('access_token')
        old_password_md5 = self.parameters.get('old_password_md5', '')
        new_password_md5 = self.parameters.get('new_password_md5', '')
        nickname = self.parameters.get('nickname', '')
        sex = self.parameters.get('sex', '')
        mail = self.parameters.get('mail', '')

        user_id = ObjectId(user_id)
        user = User.objects(id=user_id, access_token=access_token, deleted=False).first()
        if not user:
            return self.response_fail(HttpCode.fail, '用户名或密码不正确，请重新输入！')
        has_changed = False
        if old_password_md5 and old_password_md5 == user.password_md5:
            if new_password_md5 and new_password_md5 != user.password_md5:
                user.password_md5 = new_password_md5
                has_changed = True
        if nickname and nickname != user.nickname:
            user.nickname = nickname
            has_changed = True
        if sex and sex != user.sex:
            user.sex = int(sex)
            has_changed = True
        if mail and mail != user.mail:
            user.mail = mail
            has_changed = True
        if has_changed:
            user.save()
        ret = self.process_mongo_to_python(user, pop_keys=['password_md5', 'deleted'])
        return self.response_success(ret)

    @parameters(
        user_id=check(type=str, null=False),
        access_token=check(type=str, null=False)
    )
    def info(self):
        user_id = self.parameters.get('user_id')
        access_token = self.parameters.get('access_token')
        user_id = ObjectId(user_id)
        user = User.objects(id=user_id, access_token=access_token, deleted=False).first()
        if not user:
            return self.response_fail(HttpCode.fail, '用户名或密码不正确，请重新输入！')
        ret = self.process_mongo_to_python(user, pop_keys=['password_md5', 'deleted'])
        return self.response_success(ret)