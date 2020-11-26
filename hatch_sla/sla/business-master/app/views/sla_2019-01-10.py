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

def get_common_value():
    common_value_json = {}
    ## 获取通用指标
    mysql_object = MySQL_query()
    start_time, end_time, old_time, query_time = get_time()
    url = request.url  
    url = url.split('?')[0] 
    #path = request.path
    none_url = url.split('sla')[0] 
    none_sql = "select count(*) from domain where subbusiness_id is null"
    none_count = mysql_object.sql_query(none_sql, 'cmdb')[0][0]  #补充信息, for ava.html
    
    return  url, none_url, none_count, start_time, end_time, old_time, query_time


def sla_subbusiness(business_name, subbusiness_name, start_time, end_time, old_time, query_time):
    mysql_object = MySQL_query()
   
    print("subbusinesssubbusinesssubbusinesssubbusinesssubbusinesssubbusiness")   
    sql = "select domain.name as domain_name, domain.person_duty as domain_person from domain   \
               left join subbusiness on domain.subbusiness_id=subbusiness.id  \
               left join business on business.id=subbusiness.business_id where business.name='%s' and subbusiness.name='%s'" % (business_name, subbusiness_name)
    print(sql)
    fields = ['domain_name', 'domain_person']
    domains = mysql_object.mysql_RowProxy_to_list(sql, fields, 'cmdb')
    
    if domains:
        cache_object = Cache_query() 
        # 判断是否有缓存，在加一级缓存
        cache_key = "007_" + query_time + "_" + start_time + "__sla_" + business_name + "_" + subbusiness_name
        print(cache_key)
        cache = cache_object.get_redis(cache_key)
        if cache:
            print("subbusinesssubbusinesssubokokokookokokokokokokkkokookokokokokok")
            result = eval(cache)
        else:
            domain_good = domain_all = domain_1 = ""
            ### 循环拼接每个域名定义的可用性指标
            for i in range(len(domains)):
                domain_name = domains[i]['domain_name']
                domain_person = domains[i]['domain_person']
                
                if domain_name == "ams.guazi.com":
                    domain_1 = "or (domain='" + domain_name + "' and (status<498 or status=499.0) )"
                else:                
                    domain_good =  domain_good + "'" + domain_name + "', "

                domain_all = domain_all + "'" + domain_name + "', "

            domain_all = "domain in (" + domain_all.rstrip(', ')  + ")"
            
            domain_good = "(domain in (" +  domain_good.rstrip(', ') + ") and status<499.1) "
            domain_goods = domain_good +  domain_1
            #print(domain_all)
            #print(domain_goods)
            #print("cccccccccccccccccccccccccc")

            bigdata_sql = "select domain , \
                           ifnull (sum(case when  %s   and date>'%s' and date<='%s' then count end), 0)  log_all , \
                           ifnull (sum(case when (%s)  and date>'%s' and date<='%s' then count end), 0)  log_good , \
                           ifnull (sum(case when  %s   and date>'%s' and date<='%s' then count end), 0)  last_log_all , \
                           ifnull (sum(case when (%s)  and date>'%s' and date<='%s' then count end), 0)  last_log_good  \
                           from nginx_access_aggr where %s group by domain"  % \
                           (domain_all, old_time, end_time, domain_goods, old_time, end_time, domain_all, end_time, start_time, domain_goods, end_time, start_time, domain_all)
            print(bigdata_sql)

            bigdata_fields = ['domain', 'log_all', 'log_good', 'last_log_all', 'last_log_good']
            domains_sla = mysql_object.mysql_RowProxy_to_list(bigdata_sql, bigdata_fields, 'bigdata')
        
            result = []
            if domains_sla:
                ### 循环组合每个域名为 列表 json 格式
                for i in range(len(domains_sla)):
                    result_json = {}
                    result_json['domain_name'] = domains_sla[i]['domain']
                    result_json['log_all'] = int(domains_sla[i]['log_all'])
                    result_json['log_good'] = int(domains_sla[i]['log_good'])
                    result_json['last_log_all'] = int(domains_sla[i]['last_log_all'])
                    result_json['last_log_good'] = int(domains_sla[i]['last_log_good'])
                    result_json['log_all'] = int(domains_sla[i]['log_all'])
                    
                    ### 判定 0 访问量的可用性为 0，同时解决分母为0的情况
                    if domains_sla[i]['log_all'] == 0:
                        print("log_all 分母等于0")
                        result_json['log_ava'] = 0.0
                    else:
                        result_json['log_ava'] =  float('%.6f' % (result_json['log_good']/result_json['log_all']*100.0 )) 

                    if domains_sla[i]['last_log_all'] == 0:
                        print("last_log_all 分母等于0")
                        result_json['last_log_ava'] = 0.0
                    else:
                        result_json['last_log_ava'] = float('%.6f' % (result_json['last_log_good']/result_json['last_log_all']*100.0 )) 
                 
                    result_json['difference_ava'] = float('%.7f' % (result_json['last_log_ava'] - result_json['log_ava'] )) 
                    result.append(result_json)
       
                ## 存到redis
                print("subbusinesssubbusinnonononononoonononononoonononnonoononon")
                result.sort(key=lambda  x:(x['last_log_ava'],x['difference_ava']), reverse=False)
                cache_object.set_redis(cache_key, result)
        print(result)
        return result


def sla_business(business_name, start_time, end_time, old_time, query_time):
    print("进入 business 进入 business 进入 business 进入 business ")
    cache_object = Cache_query() 
    ### 判断是否有缓存，在加一级缓存
    cache_key = "007_" + query_time + "_" + start_time + "__sla_" + business_name
    print(cache_key)
    cache = cache_object.get_redis(cache_key)
    if cache:
        print("businessbusinessbusinessbusinessokokokookokokokokokokookokokookokookokokookokk")
        result = eval(cache)
    else:   
        mysql_object = MySQL_query()
        sql = "select subbusiness.name, subbusiness.person, subbusiness.name_english as name_english, business.name as business, business.name as name_main from subbusiness  \
                    left join business on business.id=subbusiness.business_id where business.name='%s'" % business_name
    
        print(sql)
        fields = ['name', 'person', 'name_english', 'business', 'name_main']
        sql_result = mysql_object.mysql_RowProxy_to_list(sql, fields, 'cmdb')
        #print(sql_result)
    
        result = []
        for i in range(len(sql_result)):
            result_json = {}
            print(sql_result[i])
            name = sql_result[i]['name']
            person = sql_result[i]['person']
            business = sql_result[i]['business']
            name_english = sql_result[i]['name_english']
            name_main = sql_result[i]['name_main']
    
            print(name, name_english, name_main)
            print("name, name_english, name_main")
            ### 循环 下一级 函数取数据
            result_mid = sla_subbusiness(name_main, name, start_time, end_time, old_time, query_time)
            
            if result_mid:
                #### 重新计算 可用性
                log_all = last_log_all = log_good = last_log_good = log_ava = last_log_ava = 0
                result_mid_count = len(result_mid)
        
                for i in range(result_mid_count):
                    log_all = log_all + result_mid[i]['log_all']
                    last_log_all = last_log_all + result_mid[i]['last_log_all']
                    log_good = log_good + result_mid[i]['log_good']
                    last_log_good = last_log_good + result_mid[i]['last_log_good']
                    log_ava = log_ava + result_mid[i]['log_ava']
                    last_log_ava = last_log_ava + result_mid[i]['last_log_ava']
                
                ### 组合 sla 列表
                result_json['name'] = name
                result_json['name_english'] = name_english
                result_json['domain_count'] = result_mid_count
                result_json['person'] = person
                result_json['log_all'] = log_all
                result_json['log_good'] = log_good
                result_json['last_log_all'] = last_log_all
                result_json['last_log_good'] = last_log_good
                
                result_json['log_ava'] = float('%.6f' % (log_ava/result_mid_count))  
                result_json['last_log_ava'] = float('%.6f' % (last_log_ava/result_mid_count)) 
                result_json['difference_ava'] = float('%.7f' % ( result_json['last_log_ava'] - result_json['log_ava'] ))
                result.append(result_json)
        
        result.sort(key=lambda  x:(x['last_log_ava'],x['difference_ava']), reverse=False)
        print("businessbusinessbusinessbusinessnonononononoononononononononono")
        cache_object.set_redis(cache_key,result)
    print(result)
    return result
    

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
            log_all = last_log_all = log_good = last_log_good = log_ava = last_log_ava = domain_count = 0
            result_mid_count = len(result_mid)
    
            for i in range(result_mid_count):
                domain_count = domain_count + result_mid[i]['domain_count']
                log_all = log_all + result_mid[i]['log_all']
                last_log_all = last_log_all + result_mid[i]['last_log_all']
                log_good = log_good + result_mid[i]['log_good']
                last_log_good = last_log_good + result_mid[i]['last_log_good']
                log_ava = log_ava + result_mid[i]['log_ava']
                last_log_ava = last_log_ava + result_mid[i]['last_log_ava']
            
            ### 组合 sla 列表
            result_json['name'] = name
            result_json['name_english'] = name_english

            result_json['person'] = person
            result_json['log_all'] = log_all
            result_json['log_good'] = log_good
            result_json['last_log_all'] = last_log_all
            result_json['last_log_good'] = last_log_good
            result_json['domain_count'] = domain_count
            result_json['log_ava'] = float('%.6f' % (log_ava/result_mid_count))  
            result_json['last_log_ava'] = float('%.6f' % (last_log_ava/result_mid_count)) 
            result_json['difference_ava'] = float('%.7f' % (result_json['last_log_ava'] - result_json['log_ava'] )) 
            result.append(result_json)

    return result

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

        mysql_object = MySQL_query()
        sql = "select name, person_duty as person, name_english, name as business, 'sla' as name_main from business"
        fields = ['name', 'person', 'name_english', 'business', 'name_main']
        sql_result = mysql_object.mysql_RowProxy_to_list(sql, fields, 'cmdb')
    
        mid = int(len(sql_result)/2)
        threads = []
        t1 = MyThread(many_process, args=(0,mid, sql_result, start_time, end_time, old_time, query_time))
        threads.append(t1)
        t2 = MyThread(many_process, args=(mid, mid+mid, sql_result, start_time, end_time, old_time, query_time))
        threads.append(t2)
        t3 = MyThread(many_process, args=(mid+mid, len(sql_result), sql_result, start_time, end_time, old_time, query_time))
        threads.append(t3)
        print(threads)
   
        result = []
        for t in threads:
            t.setDaemon(True)
            t.start()
        
        ##join所完成的工作就是线程同步，即主线程任务结束之后，进入阻塞状态，一直等待其他的子线程执行结束之后
        for t in threads:
            t.join()  
            print("进入县城跑")
            result = result + t.get_result()

        #result = []
        #for i in range(len(sql_result)):
        #    result_json = {}
        #    print(sql_result[i])
        #    name = sql_result[i]['name']
        #    person = sql_result[i]['person']
        #    business = sql_result[i]['business']
        #    name_english = sql_result[i]['name_english']
        #    name_main = sql_result[i]['name_main']
    
        #    #### 判断 英文简写是否为空
        #    if (name_english is not None) and (name_english != "None"):
        #        print(name, name_english)
        #        print("一级业务线不为空")
        #        ### 循环 下一级 函数取数据
        #        result_mid = sla_business(name_english, start_time, end_time, old_time, query_time)
        #        
        #        if result_mid:
        #            #### 重新计算 可用性
        #            log_all = last_log_all = log_good = last_log_good = log_ava = last_log_ava = 0
        #            result_mid_count = len(result_mid)
        #            print(result_mid_count)
        #
        #            for i in range(result_mid_count):
        #                log_all = log_all + result_mid[i]['log_all']
        #                last_log_all = last_log_all + result_mid[i]['last_log_all']
        #                log_good = log_good + result_mid[i]['log_good']
        #                last_log_good = last_log_good + result_mid[i]['last_log_good']
        #                log_ava = log_ava + result_mid[i]['log_ava']
        #                last_log_ava = last_log_ava + result_mid[i]['last_log_ava']
        #            
        #            ### 组合 sla 列表
        #            result_json['name'] = name
        #            result_json['name_english'] = name_english
        #            result_json['person'] = person
        #            result_json['log_all'] = log_all
        #            result_json['log_good'] = log_good
        #            result_json['last_log_all'] = last_log_all
        #            result_json['last_log_good'] = last_log_good
        #            
        #            result_json['log_ava'] = round(log_ava/result_mid_count, 6)
        #            result_json['last_log_ava'] = round(last_log_ava/result_mid_count, 6)
        #            result_json['difference_ava'] = round(result_json['last_log_ava'] - result_json['log_ava'], 6)
        #            result.append(result_json)
        #    else:
        #        print(name, name_english)
        #        print("一级业务线简写英文简写为空")

        result.sort(key=lambda  x:(x['last_log_ava'],x['difference_ava']), reverse=False)
        print("slaslaslaslaslaslaslaslanonononononononoonononononononononoononono")
        cache_object.set_redis(cache_key,result)
        rlock.release()   ### 解锁
        print(result)
    if result:    
        return render_template('sla.html', re=result, url=url, none_url=none_url, none_count=none_count, query_time=query_time)
    else:
        return Response("没有数据，或数据匹配不上，需要业务线简写 和 域名对应业务线关系", mimetype='application/json')


def html_sla_business(business_name):
    url, none_url, none_count, start_time, end_time, old_time, query_time = get_common_value()
    result = sla_business(business_name, start_time, end_time, old_time, query_time)

    if result:    
        print(url, none_url, none_count, start_time, end_time, old_time, query_time)
        return render_template('sla.html', re=result, url=url, none_url=none_url, none_count=none_count, query_time=query_time)
    else:
        return Response("没有数据，或数据匹配不上，需要业务线简写 和 域名对应业务线关系", mimetype='application/json')


def html_sla_subbusiness(business_name, subbusiness_name):
    url, none_url, none_count, start_time, end_time, old_time, query_time = get_common_value()
    result = sla_subbusiness(business_name, subbusiness_name, start_time, end_time, old_time, query_time)

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
    #              last_log_all AS (select domain,count(*) as last_access_all from nginx_access where dt > '%s' and dt <= '%s' and domain in (%s) group by domain), \
    #              last_log_good AS (select domain,count(*) as last_access_good from nginx_access where dt > '%s' and dt <= '%s' and domain in (%s) and status < 499 group by domain ), \
    #              log_result AS (select   last_log_good.last_access_good as last_access_good, last_log_all.last_access_all as last_access_all, \
    #                            COALESCE(TRY(last_log_good.last_access_good * 100.000000 / last_log_all.last_access_all), 0) AS last_access_ava from last_log_all  \
    #                            join  last_log_good on last_log_good.domain=last_log_all.domain) select domain,  * from log_result " %  \
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








