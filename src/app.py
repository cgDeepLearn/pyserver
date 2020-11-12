#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File : app.py 
# @Author : cgDeepLearn
# @Create Date : 2020/11/12-2:47 下午


from gevent import monkey
monkey.patch_all()

from traceback import format_exc
from werkzeug.wrappers import Request, Response
from werkzeug.exceptions import HTTPException, NotFound, MethodNotAllowed, BadRequest
from server import g_server
from utils.log import logger
from decorator import url_map


def g_app(environ, start_response):
    request = Request(environ)
    adapter = url_map.bind_to_environ(environ)
    try:
        endpoint, values = adapter.match()
        response = getattr(g_server, endpoint)(request, **values)
    except (NotFound, MethodNotAllowed, BadRequest) as e:
        response = e
    except HTTPException as e:
        response = e
    except:
        Response()
        response = Response('Uncatched Error')
        logger.error('app uncatched error, exception:%s', format_exc())
    return response(environ, start_response)
