#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File : api.py 
# @Author : cgDeepLearn
# @Create Date : 2020/11/16-3:40 下午

import datetime
import random


class TestApi(object):
    def __init__(self, req_data):
        self.req_data = req_data

    def process(self):
        """
        处理返回
        """
        results = [-1, 0, 1]
        res = {
            'timestamp': datetime.datetime.now().timestamp(),
            'result': random.choice(results)
        }
        return res
