# -*- coding: utf-8 -*-
import json
from datetime import date, datetime

from bson import ObjectId
from mongoengine import *
from mongoengine.base import *
from mongoengine.queryset.base import BaseQuerySet

__author__ = 'renpan'


class MongoExtend(object):
    @classmethod
    def mongo_to_python(cls, data, pop_keys=[], date_format='%Y-%m-%d %H:%M:%S'):
        def process(d):
            if isinstance(d, BaseQuerySet) or isinstance(d, BaseList) or isinstance(d, list):
                d_list = []
                for dd in d:
                    _d = process(dd)
                    d_list.append(_d)
                return d_list
            elif isinstance(d, BaseDocument):
                dd = dict()
                for field, _field in d._db_field_map.items():
                    if pop_keys and _field in pop_keys:
                        continue
                    # if field == 'id':
                    #     _field = '_id'
                    #     dd[_field] = process(d[field])
                    # else:
                    dd[_field] = process(d[field])
                return dd
            else:
                if isinstance(d, ObjectId):
                    return str(d)
                elif isinstance(d, (date, datetime)):
                    return d.strftime(date_format)
                else:
                    return d
        return process(data)

    @classmethod
    def mongo_to_python_push_keys(cls, data, push_keys=[], date_format='%Y-%m-%d %H:%M:%S'):
        def process(d):
            if isinstance(d, BaseQuerySet) or isinstance(d, BaseList) or isinstance(d, list):
                d_list = []
                for dd in d:
                    _d = process(dd)
                    d_list.append(_d)
                return d_list
            elif isinstance(d, BaseDocument):
                dd = dict()
                for field, _field in d._db_field_map.items():
                    if push_keys and _field not in push_keys:
                        continue
                    # if field == 'id':
                    #     _field = '_id'
                    #     dd[_field] = process(d[field])
                    # else:
                    dd[_field] = process(d[field])
                return dd
            else:
                if isinstance(d, ObjectId):
                    return str(d)
                elif isinstance(d, (date, datetime)):
                    return d.strftime(date_format)
                else:
                    return d
        return process(data)

    @classmethod
    def mongo_to_json(cls, data, pop_keys=[], date_format='%Y-%m-%d %H:%M:%S'):
        def process_son_to_json(obj, date_format=date_format):
            if isinstance(obj, (date, datetime)):
                return obj.strftime(date_format)
            elif isinstance(obj, ObjectId):
                return str(obj)
            else:
                raise Exception('MongoExtend: 不能识别的格式')
        data = cls.mongo_to_python(data, pop_keys=pop_keys)
        return json.dumps(data, default=process_son_to_json,
                          ensure_ascii=False)  # 这里调节ensure_ascii可以改变中文输出的时候是中文字符还是unicode字符串

    @classmethod
    def mongo_to_json_push_keys(cls, data, push_keys=[], date_format='%Y-%m-%d %H:%M:%S'):
        def process_son_to_json(obj, date_format=date_format):
            if isinstance(obj, (date, datetime)):
                return obj.strftime(date_format)
            elif isinstance(obj, ObjectId):
                return str(obj)
            else:
                raise Exception('MongoExtend: 不能识别的格式')

        data = cls.mongo_to_python_push_keys(data, push_keys=push_keys)
        return json.dumps(data, default=process_son_to_json,
                          ensure_ascii=False)  # 这里调节ensure_ascii可以改变中文输出的时候是中文字符还是unicode字符串
