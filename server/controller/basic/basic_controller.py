from sanic.response import json, text

from controller.basic import HttpCode
from libs.mongo_extend import MongoExtend
from models.User import User


class BasicController(object):
    """
    基类
    """
    def __init__(self, req, action):
        self.req = req
        self.action = action
        self.files = []
        self.params = self.find_params()
        self.parameters = dict()
        print(self.params)

    def find_params(self):
        if self.req.method == 'OPTIONS':
            return {}
        params = self.req.raw_args
        if params:
            return params
        try:
            params = self.req.json
            if params:
                return params
            else:
                return {}
        except:
            params = self.req.form
            self.files = self.req.files
            _params = params
            for k, v in _params.items():
                print(k, v)
                params[k] = v[0]
            return dict(params)

    def is_path_need_check_token(self, path):
        plist = ['/api/user/login', '/api/user/create']
        has = False
        for p in plist:
            has = path.find(p)
            if has > -1:
                break
        return has

    def execute_method(self, name):
        if self.req.method == 'OPTIONS':
            return self.response_success()
        try:
            token = self.params.get('access_token', '')
            has = self.is_path_need_check_token(self.req.path)
            user = self.check_token_available(token)
            if not user and has == -1:
                return self.response_fail(HttpCode.auth_error, '登录令牌已失效，请重新登录')
            else:
                if self.check_api_has_access(user) or has > -1:
                    return getattr(self, name)()
                else:
                    return self.response_fail(HttpCode.fail, '您没有权限访问')
        except Exception as e:
            print(e)
            return self.response_fail(HttpCode.fail, 'there is no %s function' % name)

    def process(self):
        return self.execute_method(self.action)

    def process_mongo_to_python(self, data, pop_keys=[]):
        return MongoExtend.mongo_to_python(data, pop_keys=pop_keys)

    def response_success(self, data=None):
        return self.response(code=HttpCode.success, data=data)

    def response_fail(self, code=HttpCode.fail, msg=''):
        return self.response(code=code, msg=msg)

    def response(self, code=HttpCode.success, msg='', data=None):
        result = dict(code=code, msg=msg, data=data)
        print(result)
        return json(result, headers={'Access-Control-Allow-Credentials': True},)

    def response_text(self, content):
        # result = text(content, content_type='text/xml; charset=utf-8')
        result = text(content)
        print(content)
        return result

    def check_token_available(self, token) -> User:
        user = User.objects(access_token=token, deleted=False).first()
        return user

    def check_api_has_access(self, user) -> bool:
        return True