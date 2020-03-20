# -*- coding: utf-8 -*-
from mongoengine import connect

from config.setting import AppSetting

__author__ = 'renpan'

def init_db():
    database = AppSetting.get_database_info()
    connect(database['name'], host=database['host'], port=database['port'])
    # connect(database['name'], host=database['remote_host'], port=database['remote_port'])
    return True


init_db()
