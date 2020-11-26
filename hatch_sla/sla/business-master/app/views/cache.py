
from flask import  render_template, Response, request
from app.db import  Cache_query
import json



## 查看所有 kys
def get_redis_keys():
    cache_object = Cache_query()
    result = cache_object.get_redis_keys()
    result.sort()
    url = request.url
    return render_template('sla_cache.html', re=result, url=url)


## 自定义查看key
def get_redis_key_custom(key):
    cache_object = Cache_query()
    print("get_redis_key_customget_redis_key_customget_redis_key_customget_redis_key_customget_redis_key_custom")
    if key == "all":
        result = cache_object.get_redis_keys()
    else:
        result = cache_object.get_redis(key)
    
    if result:
        return Response(json.dumps(result, indent=3, ensure_ascii=False), mimetype='application/json')
    else:
        return Response("输入错误", mimetype='application/json')

## 自定义删除某些keys
def del_redis_key_custom(key):
    cache_object = Cache_query()
    print("del_redis_key_customdel_redis_key_customdel_redis_key_custom")

    if key == "all":
        result = cache_object.del_redis_flush()
    else:
        result = cache_object.del_redis_key_custom(key)
    
    if result:
        url = request.url.split('/delete')[0]
        return render_template('rewrite.html', url=url)
    else:
        return Response("输入错误", mimetype='application/json')




