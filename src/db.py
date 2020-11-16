#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File : db.py 
# @Author : cgDeepLearn
# @Create Date : 2020/11/16-3:30 下午


import redis
from conf import config
import pymysql
from DBUtils.PooledDB import PooledDB
from utils.log import logger


class RedisOps(object):
    FIELD_EXIST = 0
    NEW_FIELD = 1

    def __init__(self, host, port, password, db):
        rd = redis.ConnectionPool(host=host, port=port, password=password, db=db)
        self.rd = redis.Redis(connection_pool=rd)


class MysqlOps(object):

    def __init__(self, host, port, user, passwd, db):
        self.pool = PooledDB(
            pymysql,
            mincached=10,
            maxcached=30,
            maxconnections=0,
            host=host,
            user=user,
            passwd=passwd,
            db=db,
            port=port,
            charset='utf8')
        self.user_apply = 'user_apply'
        self.user_base = 'user_base'
        self.flows = 'flows'
        self.table_list = list()

    def _execute(self, sql, values):
        '''
        每次都使用新的连接池中的链接
        '''
        conn = self.pool.connection()
        cur = conn.cursor()
        cur.execute(sql, values)
        conn.commit()
        conn.close()
        return cur

    def _check_parameter(self, sql, values):
        count = sql.count('%s')
        if count > 0:
            for elem in values:
                if not elem:
                    return False
        return True

    def _get_table_list(self):
        if len(self.table_list) == 0:
            sql = '''SELECT COUNT(id) FROM data_split_info'''
            table_num = list(self.select(sql))[0][0]
            self.table_list = [num for num in range(0, table_num)]

    def _replace(self, sql, table, num):
        if num == 0:
            if table in sql:
                string = ' AND %s.deleted_at is null' % table
                sql = sql + string
        else:
            pattern = '%s' % table
            string = '%s_%d' % (table, num)
            sql = sql.replace(pattern, string)
        return sql

    def _mulselect(self, apply_id, sql, values):
        self._get_table_list()

        mulcur = list()
        for num in self.table_list:
            temp_c = 0
            sql_tmp = sql
            sql_tmp = self._replace(sql_tmp, self.user_apply, num)
            sql_tmp = self._replace(sql_tmp, self.user_base, num)
            sql_tmp = self._replace(sql_tmp, self.flows, num)

            cur = self._execute(sql_tmp, values)
            for row in cur:
                temp_c = temp_c + 1
                mulcur.append(row)
            logger.info('apply_id:%d _mulselect sql:%s, values:%s, result:%s',
                        apply_id, sql_tmp, values, temp_c)

        return mulcur

    def mulselect(self, sql, values=[], apply_id=0, check=False, log=True):
        '''
        多表查询接口
        1、支持mysql基本查询，不支持聚集函数和分组排序等
        '''
        sql = sql.replace('\n', '')
        if check and not self._check_parameter(sql, values):
            return
        if log:
            logger.info('apply_id:%d mulselect sql:%s, values:%s', apply_id,
                        sql, values)
        cur = self._mulselect(apply_id, sql, values)
        for row in cur:
            yield row

    def sinselect(self, sql, values=[], apply_id=0, check=False, log=True):
        sql = sql.replace('\n', '')
        if check and not self._check_parameter(sql, values):
            return
        #过渡期间，增加deleted_at值判断
        sql = self._replace(sql, self.user_apply, num=0)
        sql = self._replace(sql, self.user_base, num=0)
        sql = self._replace(sql, self.flows, num=0)

        if log:
            logger.info('apply_id:%d sinselect sql:%s, values:%s', apply_id,
                        sql, values)
        cur = self._execute(sql, values)
        for row in cur:
            yield row

    def select(self, sql, values=[], apply_id=0, check=False, log=True):
        sql = sql.replace('\n', '')
        if check and not self._check_parameter(sql, values):
            return
        if log:
            logger.info('apply_id:%d select sql:%s, values:%s', apply_id, sql,
                        values)
        cur = self._execute(sql, values)
        for row in cur:
            yield row

    def execute(self, sql, values=[], apply_id=0, check=False, log=True):
        sql = sql.replace('\n', '')
        if check and not self._check_parameter(sql, values):
            return
        if log:
            logger.info('apply_id:%d execute sql:%s, values:%s', apply_id, sql,
                        values)
        cur = self._execute(sql, values)


redis_op = RedisOps(
    host=config.redis_host, port=config.redis_port, password=config.redis_pwd, db=config.redis_db)


mysql_op = MysqlOps(
    host=config.mysql_host,
    port=config.mysql_port,
    user=config.mysql_user,
    passwd=config.mysql_pwd,
    db=config.mysql_db)


if __name__ == '__main__':
    print(dir(redis_op))
    print(dir(mysql_op))