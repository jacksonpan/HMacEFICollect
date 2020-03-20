# -*- coding: utf-8 -*-
__author__ = 'renpan'


class AppSetting(object):
    @classmethod
    def get_host(cls):
        host = '0.0.0.0'
        return host

    @classmethod
    def get_remote_host(cls):
        host = '0.0.0.0'
        return host

    @classmethod
    def get_domain(cls):
        return "http://127.0.0.1"

    @classmethod
    def get_port(cls):
        port = 8288
        return port

    @classmethod
    def get_database_info(cls):
        db = dict(
            name="HMacEFICollect",
            host=cls.get_host(),
            port=27017,
            remote_host=cls.get_remote_host(),
            remote_port=6611
        )
        return db

    @classmethod
    def get_weixin_app_id(cls):
        return ""

    @classmethod
    def get_weixin_app_secret(cls):
        return ""

    @classmethod
    def get_weixin_token(cls):
        return ""

    @classmethod
    def get_weixin_encoding_aes_key(cls):
        return ""