#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File : gunicorn_config.py 
# @Author : cgDeepLearn
# @Create Date : 2020/11/12-3:17 下午


import os
import datetime

server_ip = '127.0.0.1'
# linux get ip
# server_ip = os.popen('ifconfig eth0|grep inet|grep -v 127.0.0.1|grep -v inet6|awk \'{print $2}\'|tr -d "addr:"').readlines()[0].strip('\r\n')
server_port = 50001
bind = '%s:%s' % (server_ip, server_port)
workers = 1  # 工作进程数

backlog = 2048  # the maximum number of pending connections
worker_connections = 2048  # the maximum number of simultaneous clients
worker_class = 'gevent'


loglevel = 'info'
# daemon = False
script_path = os.path.dirname(os.path.abspath(__file__))
work_path = os.path.dirname(script_path)
log_name = 'server'
pidfile = '{}/gunicorn.pid'.format(script_path)
errorlog = '{}/log/gunicorn_error.log'.format(work_path)
chdir = '{}/src'.format(work_path)


def worker_exit(server, worker):
    pid = worker.pid
    logfile = os.path.join(work_path, 'log/{}.{}.log'.format(log_name,pid))
    newfile = os.path.join(work_path, 'log/{}.{}.log.{}'.format(log_name,
        pid, datetime.datetime.now().strftime('%Y-%m-%d')))
    if os.path.exists(logfile):
        os.rename(logfile, newfile)