#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File : errors.py 
# @Author : cgDeepLearn
# @Create Date : 2020/11/12-2:53 下午


class gServerError(Exception):
    pass


class PostError(Exception):
    '''
    不是post请求或者post_data为空
    '''

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class ParameterError(gServerError):
    '''
    参数错误
    '''

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class HttpPathError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class ApplyDetailLack(gServerError):
    '''
    apply detail获取中关键参数没有
    '''

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class ServerProcessError(gServerError):
    def __init__(self, desc):
        self.desc = desc

    def __str__(self):
        return "错误: [%s] " % (self.desc)
