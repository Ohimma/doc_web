# -*- coding: utf-8 -*-

import datetime
from flask import request


def get_days(start_time, n):
    end_time = (start_time - datetime.timedelta(days = n )).strftime('%Y-%m-%d')
    old_time = (start_time - datetime.timedelta(days = n + n )).strftime('%Y-%m-%d')
    #date_from = datetime.datetime(day.year, day.month, day.day, 0, 0, 0)
    #date_to = datetime.datetime(day.year, day.month, day.day, 23, 59, 59)
    return end_time, old_time
    
def get_time():
    query_time = request.args.get("query_time", "")

    if query_time:
        if query_time == '3d':
            n = 3
            start_time = (datetime.datetime.now() - datetime.timedelta(days = 1))
        elif query_time == '7d':
            n = 7
            weekday = int(datetime.datetime.now().strftime('%w'))
            start_time = (datetime.datetime.now() - datetime.timedelta(days = weekday))    
        elif query_time == '30d':
            n = 1
            monthday = int(datetime.datetime.now().strftime('%d'))
            start_time = (datetime.datetime.now() - datetime.timedelta(days = monthday))
        else:
            n = 7
            start_time = (datetime.datetime.now() - datetime.timedelta(days = 1))  #昨天开始算
            query_time='7d'
        
    else:    
       n = 7
       start_time = (datetime.datetime.now() - datetime.timedelta(days = 1))  #昨天开始算
       query_time = "7d"
        
    end_time, old_time = get_days(start_time, n)
    start_time = start_time.strftime('%Y-%m-%d')

    #print(cache_time, end_time, old_time, query_time)
    return start_time, end_time, old_time, query_time
 





