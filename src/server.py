#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File : server.py 
# @Author : edgar.chen
# @Create Date : 2020/11/12-2:47 下午

import os
import json
import uuid
from werkzeug.wrappers import Response
from werkzeug.exceptions import BadRequest
from traceback import format_exc

from conf import config
from utils.log import logger, init_log
from utils.errors import ServerProcessError, ParameterError
from decorator import timer, expose


class Server(object):

    def __init__(self):
        self._pid = os.getpid()

        os.makedirs(config.log_path) if not os.path.exists(config.log_path) else None
        log_name = "{}.{}".format(config.log_name, self._pid)
        init_log(config.log_path, log_name)
        logger.debug('server is running...')

    def _rsp_encode(self, rsp):
        return json.dumps(rsp, separators=(',', ':'))

    def _req_decode(self, req):
        try:
            data = json.loads(req)
            return data
        except Exception:
            raise ParameterError("post data not json string!")

    def _errcode(self, code=0, msg='ok'):
        return dict(errCode=code, errMsg=msg, err_code=code, err_msg=msg)

    def _response(self, response):
        response['version'] = config.version
        encode_response = self._rsp_encode(response)
        return Response(encode_response, mimetype='application/json')

    def _get_query_args(self, data, apply_detail):
        try:
            apply_detail['order_id'] = int(data["order_id"])
        except:
            raise ParameterError('request params not complete or format not right')

    @expose('/test', methods=['POST'])
    @timer
    def api_test(self, request):

        try:
            req_id = str(uuid.uuid1())
            request_data = request.get_data()
            if not request_data:
                raise BadRequest()

            logger.debug('req_id: [{}] - request:{}'.format(req_id, request_data))
            # 得到请求参数字典
            data = self._req_decode(request_data)

            # 获取需要的请求参数
            apply_detail = dict()
            apply_detail['req_id'] = req_id
            self._get_query_args(data, apply_detail)

            # 查征方
            res_data = None

            # 返回
            response = self._errcode(0)
            order_id = apply_detail["order_id"]
            result = {"order_id": order_id,
                      "uuid": req_id,
                      "data": res_data}
            response.update(result)
            logger.debug('req_id: [%s] - order_id: %s, predict_org, response:%s', req_id, order_id, response)

        except BadRequest:
            logger.error('bad request, request params needed!')

            response = self._errcode(-2, 'bad request, request params needed!')

        except ParameterError as e:
            logger.error(str(e))
            response = self._errcode(-4, str(e))

        except ServerProcessError as e:
            logger.error('req_id: [%s] - apply_id: [%s] except: %s' % (req_id, order_id, str(e)))
            response = self._errcode(-3, str(e))

        except:
            logger.error('req_id: [%s] - apply_id: [%s] except: %s' % (req_id, order_id, format_exc()))
            response = self._errcode(-1, 'server error')
        finally:
            return self._response(response)


g_server = Server()
