# -*- coding: utf-8 -*-

from flask import  render_template
from app.db import MySQL_query

def hello():
    re = [('product', '2012', '2013', '2014', '2015'), ('Matcha Latte', 41.1, 30.4, 65.1, 53.3), ('Milk Tea', 86.5, 92.1, 85.7, 83.1), ('Cheese Cocoa', 24.1, 67.2, 79.5, 86.4)]
    return render_template('hello.html', re=re)
    #return render_template('index.html')

def hello_business():
    sql = "select business.id as business_id, business.name as business_name, business.name_english as business_name_english, \
           business.person_duty as business_person, business.org_id as business_org_id , count(*) as subbusiness_count \
           from business left join subbusiness on business.id=subbusiness.business_id group by subbusiness.business_id;"
    fields = ['business_id', 'business_name', 'business_name_english', 'business_person', 'business_org_id', 'subbusiness_count']
    object = MySQL_query()
    result = object.mysql_RowProxy_to_list(sql, fields, 'cmdb')
    result.sort(key=lambda  x:(x['subbusiness_count']), reverse=False)
    print(result)
    return render_template('hello_business.html', re=result)

