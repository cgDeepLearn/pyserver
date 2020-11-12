#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File : decorator.py 
# @Author : cgDeepLearn
# @Create Date : 2020/11/12-2:56 下午

import time
from functools import wraps
from utils.log import logger
from werkzeug.routing import Map, Rule


url_map = Map()


def expose(rule, **kw):
    def decorate(f):
        kw['endpoint'] = f.__name__
        url_map.add(Rule(rule, **kw))
        return f

    return decorate


def timer(func):
    """计时装饰器"""
    @wraps(func)
    def _wraps(*args, **kwargs):
        begin = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        process_time = end - begin
        logger.debug("func: %s, process cost: %f seconds" % (func.__name__, process_time))
        return result
    return _wraps
