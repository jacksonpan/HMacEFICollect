# -*- coding: utf-8 -*-
from functools import wraps


__author__ = 'jacksonpan'

from controller.basic import HttpCode


class check(object):
    def __init__(self, **kwargs):
        """
        参数检查条件
        :param kwargs:
        type 类型，如str, int
        default 默认值，如0，1，'hello'
        name 参数名字转义，如传过来的参数名叫a，但是函数体内我们按照我们的习惯命名成了b，为了对应这里就可以设置
        null 是否为空，如True or False，默认为True
        """
        self.type = kwargs.get('type', None)
        self.default = kwargs.get('default', None)
        self.name = kwargs.get('name', None)
        self.null = kwargs.get('null', True)


class ParameterTypeException(Exception):
    pass


class ParameterExistenceException(Exception):
    pass


class ParameterProcessException(Exception):
    pass


def _convert_name(params, **expects):
    for key, value in expects.items():
        if value.name is not None:
            if value.name in params:
                params[key] = params.get(value.name)


def _check_existence(params, **expects):
    for key, value in expects.items():
        if value.null is False:
            if key not in params:
                hint = "%s can't be null" % (key)
                raise ParameterExistenceException(hint)


def _check_type(params, **expects):
    for key, value in params.items():
        if key in expects:
            check = expects[key]
            if check.type is not None:
                expect_type = check.type
                got_type = type(value)
                if got_type is not expect_type:
                    try:
                        params[key] = expect_type(value)
                    except Exception as e:
                        hint = "%s is not the expect type '%s'" % (key, expect_type)
                        raise ParameterTypeException(hint)


def _fullfill_default(params, **expects):
    for key, value in expects.items():
        if value.default is not None:
            params.setdefault(key, value.default)


def _prune_extra(params ,**expects):
    expect_parameters = dict()
    for key, value in params.items():
        if key in expects:
            expect_parameters[key] = params[key]
    return expect_parameters


def parameters(**expects):
    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            self = args[0]
            params = self.params
            # 先把如果有转义的参数先统一
            _convert_name(params, **expects)
            try:
                # 检查条件
                _check_existence(params, **expects)
                _check_type(params, **expects)
            except Exception as e:
                print(func, e)
                hint = e
                return self.response_fail(HttpCode.fail, str(hint))

            # 填入默认值
            _fullfill_default(params, **expects)
            # 组织最终参数并赋值给控制器本身，直接使用self.parameters即可调用
            self.parameters = _prune_extra(params, **expects)
            ret = func(self)
            return ret
        return wrapped
    return decorator
