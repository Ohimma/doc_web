# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy

from app.presto import presto_client
from config import config
import redis
import os

db = SQLAlchemy()
config_name = config[os.getenv('FLASK_CONFIG') or 'default']

class MySQL_query:
    def sql_query(self, sql, app):
        if app == "cmdb":
            engine = create_engine(config_name.CMDB_DATABASE_URI)
        elif app == "earthworm":
            engine = create_engine(config_name.EARTHWORM_DATABASE_URI)
        elif app == "medusa":
            engine = create_engine(config_name.MEDUSA_DATABASE_URI)
        elif app == "bigdata":
            engine = create_engine(config_name.BIGDATA_DATABASE_URL)
        else:
            engine = create_engine(config_name.CMDB_DATABASE_URI)

        connection = engine.connect()
        result = connection.execute(sql)
        
        #data = result.first()         # 获取第一行,并无条件释放链接
        #data = result.rowcount        # 获取行数
        #data = result.fetchone()      # 一行一行取出RowProxy对象,取出后释放链接
        #data = result.fetchmany()     # list 格式一行一行取出RowProxy对象,取出后释放链接
        #data = result.returns_rows    # 返回 bool 值 
        data = result.fetchall()       # list格式输出所有RowProxy对象
        connection.close()
        return data

    def mysql_RowProxy_to_str(self, sql, app):
        result_str = ""
        result = self.sql_query(sql, app)
        if result:
            for i in range(len(result)):
                result_str = result_str + "'" + result[i][0] + "' ,"
        result = result_str.strip(',')
        return result

    def mysql_RowProxy_to_list(self, sql, fields, app):
        result_list = []
        result = self.sql_query(sql, app)
        if result:
            for i in range(len(result)):
                result_json = {}
                for column_num in range(len(fields)):
                    result_json[fields[column_num]] = result[i][fields[column_num]]
                result_list.append(result_json)
        return result_list

    def orm_query():
        data = Business.query.all() 
        print(data)
        print(type(data))
        print(str(Business.query))
    

##################################################
##  http://cwiki.guazi.com/pages/viewpage.action?pageId=56561921
##################################################
class Presto_query:
    def sql_query(self, sql):
        cursor = presto_client.connect(config_name.PRESTO_DOMAIN, port=config_name.PRESTO_PORT, 
                                       username=config_name.PRESTO_USER, group=config_name.PRESTO_GROUP, password=config_name.PRESTO_PASSWORD, 
                                       catalog=config_name.PRESTO_CATALOG, schema=config_name.PRESTO_SCHEMA,).cursor()
    
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
     

    def presto_Tuple_to_list(self, sql, fields):
        result_list = []
        result = self.sql_query(sql)
        if result:
            for row_num in range(len(result)):
                result_json = {}
                to_list = list(result[row_num])
                for column_num in range(len(fields)):
                    result_json[fields[column_num]] = to_list[column_num]
                result_list.append(result_json)
        return result_list



class Cache_query:
    def conn_redis(self):
        pool = redis.ConnectionPool(host=config_name.CACHE_HOST, port=config_name.CACHE_PORT, password=config_name.CACHE_PASSWORD, db=2, decode_responses=True)
        r = redis.Redis(connection_pool=pool)
        return r

    ### 操作单个 , 插入 + 查询
    def set_redis(self, k,v):
        r = self.conn_redis()
        r.set(k,v)
        r.expire(k, 72000)

    ### 所有查询 + 单个查询
    def get_redis(self, k):
        r = self.conn_redis()
        return  r.get(k)

    def get_redis_keys(self):
        r = self.conn_redis()
        return  r.keys()
    


    ### 所有删除 + 自定义删除
    def del_redis_flush(self):
        r = self.conn_redis()
        return  r.flushdb()

    def del_redis_key_custom(self, k):
        r = self.conn_redis()
        if r.keys(k):
            print("cunzaixunzai cunzaicunzai")
            return r.delete(*r.keys(k))

            