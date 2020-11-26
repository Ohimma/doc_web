# -*- coding: utf-8 -*-

from flask import  render_template, Response, request, redirect
from app.db import  MySQL_query, Presto_query, Cache_query

from .mythread import MyThread
from .query_time import get_time

import threading
import datetime
import json
import os

rlock=threading.RLock()


def many_process(start, stop, sql_result, start_time, end_time, old_time, query_time):
    result = []
    for i in range(start, stop):
        print(start, stop)
        result_json = {}
        print(sql_result[i])
        name = sql_result[i]['name']
        person = sql_result[i]['person']
        business = sql_result[i]['business']
        name_english = sql_result[i]['name_english']
        name_main = sql_result[i]['name_main']

        print(name, name_english)
        print("name, name_english")
        ### 循环 下一级 函数取数据
        result_mid = sla_business(name, start_time, end_time, old_time, query_time)
        
        if result_mid:
            #### 重新计算 可用性
            log_all = old_log_all = log_good = old_log_good = log_ava = old_log_ava = domain_count = 0
            result_mid_count = len(result_mid)
    
            for i in range(result_mid_count):
                domain_count = domain_count + result_mid[i]['domain_count']
                log_all = log_all + result_mid[i]['log_all']
                old_log_all = old_log_all + result_mid[i]['old_log_all']
                log_good = log_good + result_mid[i]['log_good']
                old_log_good = old_log_good + result_mid[i]['old_log_good']
                log_ava = log_ava + result_mid[i]['log_ava']
                old_log_ava = old_log_ava + result_mid[i]['old_log_ava']
            
            ### 组合 sla 列表
            result_json['name'] = name
            result_json['name_english'] = name_english

            result_json['person'] = person
            result_json['log_all'] = log_all
            result_json['log_good'] = log_good
            result_json['old_log_all'] = old_log_all
            result_json['old_log_good'] = old_log_good
            result_json['domain_count'] = domain_count
            result_json['log_ava'] = float('%.6f' % (log_ava/result_mid_count))  
            result_json['old_log_ava'] = float('%.6f' % (old_log_ava/result_mid_count)) 
            result_json['difference_ava'] = float('%.7f' % (result_json['old_log_ava'] - result_json['log_ava'] )) 
            result.append(result_json)

    return result

def get_common_value():
    common_value_json = {}
    ## 获取通用指标
    start_time, end_time, old_time, query_time = get_time()    
    
    url = request.url  
    url = url.split('?')[0] 
    none_url = url.split('sla')[0] 

    mysql_object = MySQL_query()
    none_sql = "select count(*) from domain where subbusiness_id is null"
    none_count = mysql_object.sql_query(none_sql, 'cmdb')[0][0]  #补充信息, for ava.html
    
    return  url, none_url, none_count, start_time, end_time, old_time, query_time



def sla_business_subbusiness(domains, domain_count, name, person, start_time, end_time, old_time, query_time):
    mysql_object = MySQL_query()
    domain_cache = {}

    domain_count = len(domains)

    domain_good = domain_all = domain_1 = ""
    for i in range(len(domains)):
        domain_name = domains[i]['domain_name']
        domain_person = domains[i]['domain_person']
        
        if domain_name == "ams.guazi.com":
            domain_1 = "or (domain='" + domain_name + "' and (status<498 or status=499.0) )"
        else:                
            domain_good =  domain_good + "'" + domain_name + "', "

        domain_all = domain_all + "'" + domain_name + "', "

    domain_all = "domain in (" + domain_all.rstrip(', ')  + ") "
    
    domain_good = "domain in (" +  domain_good.rstrip(', ') + ") and status<499.1 "
    domain_goods = domain_good +  domain_1
    ### 获取域名的 sla

    #start_time='2018-12-31'
    #end_time = '2018-12-29'
    #old_time = '2018-12-27'
    now_time = "date<='" + start_time + "' and date>'"  + old_time + "'"
    print(now_time)
    
    bigdata_sql = "select date, \
                   ifnull (sum(count), 0)  log_all , \
                   ifnull (sum(case when %s   then count end), 0)  log_good , \
                 ((ifnull (sum(case when %s   then count end), 0)) / (ifnull (sum(count), 1)) * 100.0) log_ava \
                   from nginx_access_aggr where %s and %s group by date "  % \
                   (domain_goods, domain_goods, domain_all, now_time)
    print(bigdata_sql)
    bigdata_fields = ['date', 'log_all', 'log_good', 'log_ava']
    domains_sla = mysql_object.mysql_RowProxy_to_list(bigdata_sql, bigdata_fields, 'bigdata')
    print(domains_sla)

    if domains_sla:
        ### 计算汇总可用性
        count_log_all = count_log_good = count_old_log_all = count_old_log_good = count_log_ava = count_old_log_ava = 0
        for i in range(len(domains_sla)):
            mid_days = (len(domains_sla)/2)            
            mid_date = domains_sla[i]['date']
            print("mid_days====== %s" % mid_days)

            if  mid_date <= end_time:
                print("oldoldoldoldoldo")
                domains_sla[i]['log_all'] = int(domains_sla[i]['log_all'])
                domains_sla[i]['log_good'] = int(domains_sla[i]['log_good'])
                domains_sla[i]['log_ava'] = float(domains_sla[i]['log_ava'])
                count_old_log_all = count_old_log_all + domains_sla[i]['log_all']
                count_old_log_good = count_old_log_good + domains_sla[i]['log_good']
                count_old_log_ava = count_old_log_ava + domains_sla[i]['log_ava']
            else:
                domains_sla[i]['log_all'] = int(domains_sla[i]['log_all'])
                domains_sla[i]['log_good'] = int(domains_sla[i]['log_good'])
                domains_sla[i]['log_ava'] = float(domains_sla[i]['log_ava'])
                count_log_all = count_log_all + domains_sla[i]['log_all']
                count_log_good = count_log_good + domains_sla[i]['log_good']
                count_log_ava = count_log_ava + domains_sla[i]['log_ava']
        
        domain_cache['name'] = name
        domain_cache['person'] = person
        domain_cache['domain_count'] = domain_count
        domain_cache['count_log_all'] = count_log_all
        domain_cache['count_log_good'] = count_log_good
        domain_cache['count_log_ava'] = float('%.7f' % (count_log_ava/mid_days ))
        
        domain_cache['count_old_log_all'] = count_old_log_all
        domain_cache['count_old_log_ava'] = float('%.7f' % (count_old_log_ava/mid_days ))
        
        domain_cache['difference_ava'] = float('%.7f' % (domain_cache['count_log_ava'] - domain_cache['count_old_log_ava']))
        domain_cache['details'] = domains_sla

        #print(domain_cache)
        return domain_cache

def html_sla():
    url, none_url, none_count, start_time, end_time, old_time, query_time = get_common_value()
    print("进入 sla 进入 sla 进入 sla 进入 sla 进入 sla 进入 sla")

    cache_object = Cache_query() 
    ## 判断是否有缓存，在加一级缓存
    cache_key = "007_" + query_time + "_" + start_time + "__sla" 
    print(cache_key)
    cache = cache_object.get_redis(cache_key)
    if cache:
        print("slaslaslaslaslasla okokokookokokokokokokk")
        result = eval(cache)
    else:
        rlock.acquire()   ## 锁住，防止第二个业务线请求混淆 

        #### 获取所有一级业务线列表
        mysql_object = MySQL_query()
        sql = "select name, person_duty as person, name_english, name as business, 'sla' as name_main from business"
        fields = ['name', 'person', 'name_english', 'business', 'name_main']
        sql_result = mysql_object.mysql_RowProxy_to_list(sql, fields, 'cmdb')

        ### 根据每隔二级业务线获取所有domain，计算
        result = []
        for i in range(len(sql_result)):
            name = sql_result[i]['name']
            name_english = sql_result[i]['name_english']
            person = sql_result[i]['person']
            #business = name_main = sql_result[i]['business']
    
            sql = "select domain.name as domain_name, domain.person_duty as domain_person from domain   \
                   left join subbusiness on domain.subbusiness_id=subbusiness.id  \
                   left join business on business.id=subbusiness.business_id where business.name='%s'" % ( name)
            fields = ['domain_name', 'domain_person']
            domains = mysql_object.mysql_RowProxy_to_list(sql, fields, 'cmdb')

            if domains:
                domain_cache = sla_business_subbusiness(domains, len(domains), name, person, start_time, end_time, old_time, query_time)
                if domain_cache:
                    result.append(domain_cache)

        print("slaslalslaslaslalsla outoutoutoutoutoutoutoutoutout")
        cache_object.set_redis(cache_key,result)
        rlock.release()   ### 解锁
        result.sort(key=lambda  x:(x['count_log_ava'],x['difference_ava']), reverse=False)
        
    print(result)
    if result:    
        return render_template('sla.html', re=result, url=url, none_url=none_url, none_count=none_count, query_time=query_time)
    else:
        return Response("没有数据，或数据匹配不上，需要业务线简写 和 域名对应业务线关系", mimetype='application/json')


def html_sla_business(business_name):
    url, none_url, none_count, start_time, end_time, old_time, query_time = get_common_value()
    print("进入 business 进入 business 进入 business 进入 business ")

    cache_object = Cache_query() 
    ## 判断是否有缓存，在加一级缓存
    cache_key = "007_" + query_time + "_" + start_time + "__" + business_name 
    print(cache_key)
    cache = cache_object.get_redis(cache_key)
    if cache:
        print("slaslaslaslaslasla okokokookokokokokokokk")
        result = eval(cache)
    else:
        rlock.acquire()   ## 锁住，防止第二个业务线请求混淆 

        ### 获取所有二级业务线列表
        mysql_object = MySQL_query()
        sql = "select subbusiness.name , subbusiness.person, subbusiness.name_english as name_english, business.name as business, business.name as name_main from subbusiness  \
                    left join business on business.id=subbusiness.business_id where business.name='%s'" % business_name
    
        fields = ['name', 'person', 'name_english', 'business', 'name_main']
        sql_result = mysql_object.mysql_RowProxy_to_list(sql, fields, 'cmdb')
    
        ### 根据每隔二级业务线获取所有domain，计算
        result = []
        for i in range(len(sql_result)):
            name = sql_result[i]['name']
            name_english = sql_result[i]['name_english']
            person = sql_result[i]['person']
            business = name_main = sql_result[i]['business']
    
            sql = "select domain.name as domain_name, domain.person_duty as domain_person from domain   \
                   left join subbusiness on domain.subbusiness_id=subbusiness.id  \
                   left join business on business.id=subbusiness.business_id where business.name='%s' and subbusiness.name='%s'" % (name_main, name)
            fields = ['domain_name', 'domain_person']
            domains = mysql_object.mysql_RowProxy_to_list(sql, fields, 'cmdb')
        
            if domains:
                domain_cache = sla_business_subbusiness(domains, len(domains), name, person, start_time, end_time, old_time, query_time)
                if domain_cache:
                    result.append(domain_cache)
        
        print("businessbusinessbusinessbusbusi   outoutoutoutoutoutoutoutoutoutoutout")
        cache_object.set_redis(cache_key,result)
        rlock.release()   ### 解锁
        result.sort(key=lambda  x:(x['count_log_ava'],x['difference_ava']), reverse=False)

    print(result)
    if result:    
        print(url, none_url, none_count, start_time, end_time, old_time, query_time)
        return render_template('sla.html', re=result, url=url, none_url=none_url, none_count=none_count, query_time=query_time)
    else:
        return Response("没有数据，或数据匹配不上，需要业务线简写 和 域名对应业务线关系", mimetype='application/json')


def sla_subbusiness(business_name, subbusiness_name, start_time, end_time, old_time, query_time):
    mysql_object = MySQL_query()

    print("subbusinesssubbusinesssubbusinesssubbusinesssubbusinesssubbusiness")   
    sql = "select domain.name as domain_name, domain.person_duty as domain_person from domain   \
               left join subbusiness on domain.subbusiness_id=subbusiness.id  \
               left join business on business.id=subbusiness.business_id where business.name='%s' and subbusiness.name='%s'" % (business_name, subbusiness_name)
    fields = ['domain_name', 'domain_person']
    domains = mysql_object.mysql_RowProxy_to_list(sql, fields, 'cmdb')

    result = []
    for i in range(len(domains)):
        domain_cache = {}
        domain_name = domains[i]['domain_name']
        domain_person = domains[i]['domain_person']
        
        ### 状态码白名单机制
        if domain_name == "business.guazi-corp.com":
            domain_white_list = "504"
        else:
            domain_white_list = "499.0"
        domain_status_ava = '(status < 499 or status in (' +  domain_white_list + ' ))'

        ### 获取域名的 sla
        #start_time='2018-12-31'
        #end_time = '2018-12-29'
        #old_time = '2018-12-27'

        now_time = "date<='" + start_time + "' and date>'"  + old_time + "'"
        print(now_time)

        bigdata_sql = "select date, \
                       ifnull (sum(count), 0)  log_all , \
                       ifnull (sum(case when  %s then count end), 0)  log_good,  \
                     ((ifnull (sum(case when  %s then count end), 0)) / (ifnull (sum(count), 1)) * 100.0) log_ava \
                       from nginx_access_aggr where domain='%s' and %s group by domain, date"  % \
                       (domain_status_ava, domain_status_ava, domain_name, now_time)
        print(bigdata_sql)
        bigdata_fields = ['date', 'log_all', 'log_good', 'log_ava']
        domains_sla = mysql_object.mysql_RowProxy_to_list(bigdata_sql, bigdata_fields, 'bigdata')
        #print(domains_sla)

        if domains_sla:
            ### 计算汇总可用性
            count_log_all = count_log_good = count_old_log_all = count_old_log_good = count_log_ava = count_old_log_ava = 0
            for i in range(len(domains_sla)):
                mid_days = (len(domains_sla)/2)            
                mid_date = domains_sla[i]['date']
                if  mid_date <= end_time:
                    print("oldoldoldoldoldo")
                    domains_sla[i]['log_all'] = int(domains_sla[i]['log_all'])
                    domains_sla[i]['log_good'] = int(domains_sla[i]['log_good'])
                    domains_sla[i]['log_ava'] = float(domains_sla[i]['log_ava'])
                    count_old_log_all = count_old_log_all + domains_sla[i]['log_all']
                    count_old_log_good = count_old_log_good + domains_sla[i]['log_good']
                    count_old_log_ava = count_old_log_ava + domains_sla[i]['log_ava']
                else:
                    print("newnewnewnenwenwnwn")
                    domains_sla[i]['log_all'] = int(domains_sla[i]['log_all'])
                    domains_sla[i]['log_good'] = int(domains_sla[i]['log_good'])
                    domains_sla[i]['log_ava'] = float(domains_sla[i]['log_ava'])
                    count_log_all = count_log_all + domains_sla[i]['log_all']
                    count_log_good = count_log_good + domains_sla[i]['log_good']
                    count_log_ava = count_log_ava + domains_sla[i]['log_ava']
        
            domain_cache['name'] = domain_name
            domain_cache['person'] = domain_person
            domain_cache['count_log_all'] = count_log_all
            domain_cache['count_log_good'] = count_log_good
            domain_cache['count_log_ava'] = float('%.7f' % (count_log_ava/mid_days ))
        
            domain_cache['count_old_log_all'] = count_old_log_all
            domain_cache['count_old_log_ava'] = float('%.7f' % (count_old_log_ava/mid_days ))
            
            domain_cache['difference_ava'] = float('%.7f' % (domain_cache['count_log_ava'] - domain_cache['count_old_log_ava']))
            domain_cache['details'] = domains_sla
            result.append(domain_cache)
    
    
    print("sla_subbusinesssla_subbusinesssla_subbusinessoutoutoutoutoutoutoutoutoutoutoutout")
    result.sort(key=lambda  x:(x['count_log_ava'],x['difference_ava']), reverse=False)
    print(result)
    return result


def html_sla_subbusiness(business_name, subbusiness_name):
    url, none_url, none_count, start_time, end_time, old_time, query_time = get_common_value()

    #result = sla_subbusiness(business_name, subbusiness_name, start_time, end_time, old_time, query_time)
    result = [{'name': 'sla.guazi-corp.com', 'person': None, 'count_log_all': 41, 'count_log_good': 37, 'count_log_ava': 64.035085, 'count_old_log_all': 587, 'count_old_log_ava': 99.00647, 'difference_ava': -34.971385, 'details': [{'date': '2018-12-28', 'log_all': 351, 'log_good': 347, 'log_ava': 98.8604}, {'date': '2018-12-29', 'log_all': 236, 'log_good': 234, 'log_ava': 99.15254}, {'date': '2018-12-30', 'log_all': 3, 'log_good': 1, 'log_ava': 33.33333}, {'date': '2018-12-31', 'log_all': 38, 'log_good': 36, 'log_ava': 94.73684}]}, {'name': 'sre-grafana.guazi-corp.com', 'person': '黄飞', 'count_log_all': 7979, 'count_log_good': 7921, 'count_log_ava': 98.819855, 'count_old_log_all': 46676, 'count_old_log_ava': 99.20125, 'difference_ava': -0.381395, 'details': [{'date': '2018-12-28', 'log_all': 17706, 'log_good': 17590, 'log_ava': 99.34485}, {'date': '2018-12-29', 'log_all': 28970, 'log_good': 28697, 'log_ava': 99.05765}, {'date': '2018-12-30', 'log_all': 748, 'log_good': 735, 'log_ava': 98.26203}, {'date': '2018-12-31', 'log_all': 7231, 'log_good': 7186, 'log_ava': 99.37768}]}, {'name': 'app.guazistatic.com', 'person': None, 'count_log_all': 21323, 'count_log_good': 21321, 'count_log_ava': 99.990605, 'count_old_log_all': 20953, 'count_old_log_ava': 99.596605, 'difference_ava': 0.394, 'details': [{'date': '2018-12-28', 'log_all': 10289, 'log_good': 10288, 'log_ava': 99.99028}, {'date': '2018-12-29', 'log_all': 10664, 'log_good': 10579, 'log_ava': 99.20293}, {'date': '2018-12-30', 'log_all': 11083, 'log_good': 11082, 'log_ava': 99.99098}, {'date': '2018-12-31', 'log_all': 10240, 'log_good': 10239, 'log_ava': 99.99023}]}, {'name': 'c4.guazi-corp.com', 'person': '郝朝阳', 'count_log_all': 4313569, 'count_log_good': 4313551, 'count_log_ava': 99.999585, 'count_old_log_all': 4072614, 'count_old_log_ava': 99.9861, 'difference_ava': 0.013485, 'details': [{'date': '2018-12-28', 'log_all': 2072289, 'log_good': 2071917, 'log_ava': 99.98205}, {'date': '2018-12-29', 'log_all': 2000325, 'log_good': 2000128, 'log_ava': 99.99015}, {'date': '2018-12-30', 'log_all': 2153817, 'log_good': 2153809, 'log_ava': 99.99963}, {'date': '2018-12-31', 'log_all': 2159752, 'log_good': 2159742, 'log_ava': 99.99954}]}, {'name': 'post.guazi.com', 'person': None, 'count_log_all': 1189, 'count_log_good': 1189, 'count_log_ava': 100.0, 'count_old_log_all': 1443, 'count_old_log_ava': 100.0, 'difference_ava': 0.0, 'details': [{'date': '2018-12-28', 'log_all': 652, 'log_good': 652, 'log_ava': 100.0}, {'date': '2018-12-29', 'log_all': 791, 'log_good': 791, 'log_ava': 100.0}, {'date': '2018-12-30', 'log_all': 662, 'log_good': 662, 'log_ava': 100.0}, {'date': '2018-12-31', 'log_all': 527, 'log_good': 527, 'log_ava': 100.0}]}, {'name': 'ebs.guazi.com', 'person': None, 'count_log_all': 652, 'count_log_good': 652, 'count_log_ava': 100.0, 'count_old_log_all': 621, 'count_old_log_ava': 100.0, 'difference_ava': 0.0, 'details': [{'date': '2018-12-28', 'log_all': 268, 'log_good': 268, 'log_ava': 100.0}, {'date': '2018-12-29', 'log_all': 353, 'log_good': 353, 'log_ava': 100.0}, {'date': '2018-12-30', 'log_all': 395, 'log_good': 395, 'log_ava': 100.0}, {'date': '2018-12-31', 'log_all': 257, 'log_good': 257, 'log_ava': 100.0}]}, {'name': 'zhaopin.guazi.com', 'person': None, 'count_log_all': 6493, 'count_log_good': 6493, 'count_log_ava': 100.0, 'count_old_log_all': 6114, 'count_old_log_ava': 100.0, 'difference_ava': 0.0, 'details': [{'date': '2018-12-28', 'log_all': 2825, 'log_good': 2825, 'log_ava': 100.0}, {'date': '2018-12-29', 'log_all': 3289, 'log_good': 3289, 'log_ava': 100.0}, {'date': '2018-12-30', 'log_all': 3366, 'log_good': 3366, 'log_ava': 100.0}, {'date': '2018-12-31', 'log_all': 3127, 'log_good': 3127, 'log_ava': 100.0}]}, {'name': 'bbs.guazi-corp.com', 'person': None, 'count_log_all': 2878, 'count_log_good': 2878, 'count_log_ava': 100.0, 'count_old_log_all': 2880, 'count_old_log_ava': 100.0, 'difference_ava': 0.0, 'details': [{'date': '2018-12-28', 'log_all': 1441, 'log_good': 1441, 'log_ava': 100.0}, {'date': '2018-12-29', 'log_all': 1439, 'log_good': 1439, 'log_ava': 100.0}, {'date': '2018-12-30', 'log_all': 1439, 'log_good': 1439, 'log_ava': 100.0}, {'date': '2018-12-31', 'log_all': 1439, 'log_good': 1439, 'log_ava': 100.0}]}]

    if result:    
        print(url, none_url, none_count, start_time, end_time, old_time, query_time)
        return render_template('sla_domain.html', re=result, url=url, none_url=none_url, none_count=none_count, query_time=query_time)
    else:
        return Response("没有数据，或数据匹配不上，需要业务线简写 和 域名对应业务线关系", mimetype='application/json')
  


def sla_none():   # 只查询前三天的数据可用性
    #start_time = (datetime.datetime.now()-datetime.timedelta(days = 1)).strftime('%Y-%m-%d')
    #end_time = (datetime.datetime.now()-datetime.timedelta(days = 4 )).strftime('%Y-%m-%d')
    #start_time = "2018-10-03"
    #end_time = "2018-10-01"
    #sql = "select name from domain where subbusiness_id is null"
    #object = MySQL_query()
    #domain = object.mysql_RowProxy_to_str(sql)
    #print(domain)
    #if domain:
    #    #domain = "'" + "uc.maodou.com" + "'"
    #    sql = "WITH \
    #              old_log_all AS (select domain,count(*) as old_access_all from nginx_access where dt > '%s' and dt <= '%s' and domain in (%s) group by domain), \
    #              old_log_good AS (select domain,count(*) as old_access_good from nginx_access where dt > '%s' and dt <= '%s' and domain in (%s) and status < 499 group by domain ), \
    #              log_result AS (select   old_log_good.old_access_good as old_access_good, old_log_all.old_access_all as old_access_all, \
    #                            COALESCE(TRY(old_log_good.old_access_good * 100.000000 / old_log_all.old_access_all), 0) AS old_access_ava from old_log_all  \
    #                            join  old_log_good on old_log_good.domain=old_log_all.domain) select domain,  * from log_result " %  \
    #                            (end_time, start_time, domain, end_time, start_time, domain)
    #    print(sql)
    #    object = Presto_query()
    #    result = object.sql_query(sql)
    #    print(result)
    #    return render_template('slanone.html', re=result)
    
    #else:
    #       return Response("域名都有归属了...挺好", mimetype='application/json') 
    #return Response("别闹，去找你 SRE 玩去.....", mimetype='application/json') 
    print("entry sla_none none noene")
    sql = "select * from domain where subbusiness_id is null"
    object = MySQL_query()
    result = object.sql_query(sql, 'cmdb')
    if result:
        return render_template('sla_none.html', re=result)
    else:
        return Response("没有数据", mimetype='application/json')

def domain_info(business_name_english, subbusiness_name_english, domain):
    
    return Response("还没有东西，稍等.....", mimetype='application/json')








