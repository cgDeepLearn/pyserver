#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File : config.py 
# @Author : cgDeepLearn
# @Create Date : 2020/11/12-3:02 下午


import os
conf_path = os.path.dirname(os.path.abspath(__file__))
work_path = os.path.dirname(os.path.dirname(conf_path))
script_path = os.path.join(work_path, "script")

log_path = os.path.join(work_path, "log")
print(conf_path, work_path, script_path, log_path)
log_name = 'server'


server_port = 50001


version = "001"
