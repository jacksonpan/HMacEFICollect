# -*- coding: utf-8 -*-
__author__ = 'renpan'
from _md5 import md5


def _md5(src: str) -> str:
    return md5(src.encode()).hexdigest()
