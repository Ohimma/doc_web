# -*- coding: utf-8 -*-

from app.views import hello, api, cache, release, sla

def init_urls(app):
    app.add_url_rule('/', view_func=hello.hello_business, methods=['GET'])
    app.add_url_rule('/hello', view_func=hello.hello, methods=['GET'])

    app.add_url_rule('/api/cmdb/business', view_func=api.cmdb_business, methods=['GET'])
    app.add_url_rule('/api/cmdb/subbusiness', view_func=api.cmdb_subbusiness, methods=['GET'])
    app.add_url_rule('/api/cmdb/domain', view_func=api.cmdb_domain, methods=['GET'])
    #app.add_url_rule('/api/presto/domain', view_func=api.presto_domain, methods=['GET'])

    
    app.add_url_rule('/release', view_func=release.release, methods=['GET'])
    app.add_url_rule('/release/bak', view_func=release.release_bak, methods=['GET'])
    app.add_url_rule('/release/medusa/<business_name>', view_func=release.medusa_release_business, methods=['GET'])
    app.add_url_rule('/release/earthworm/<business_name>', view_func=release.earthworm_release_business, methods=['GET'])

    app.add_url_rule('/cache', view_func=cache.get_redis_keys, methods=['GET'])
    app.add_url_rule('/cache/get/<key>', view_func=cache.get_redis_key_custom, methods=['GET'])
    app.add_url_rule('/cache/delete/<key>', view_func=cache.del_redis_key_custom, methods=['GET'])

    app.add_url_rule('/sla/none', view_func=sla.sla_none, methods=['GET'])
    app.add_url_rule('/sla', view_func=sla.html_sla, methods=['GET'])
    app.add_url_rule('/sla/<business_name>', view_func=sla.html_sla_business, methods=['GET'])
    app.add_url_rule('/sla/<business_name>/<subbusiness_name>', view_func=sla.html_sla_subbusiness, methods=['GET'])
    #app.add_url_rule('/sla2/none', view_func=sla2.sla_none, methods=['GET'])
    #app.add_url_rule('/sla2', view_func=sla2.html_sla, methods=['GET'])
    #app.add_url_rule('/sla2/<business_name>', view_func=sla2.html_sla_business, methods=['GET'])
    #app.add_url_rule('/sla2/<business_name>/<subbusiness_name>', view_func=sla2.html_sla_subbusiness, methods=['GET'])
    #app.add_url_rule('/sla/<business_name_english>/<subbusiness_name_english>/<domain>', view_func=sla.domain_info, methods=['GET'])


#    app.add_url_rule('/api/trees/<node_id>/content',
#                     view_func=TreeContentAPI.as_view('tree_content_api'),
#                     methods=['GET', 'POST', 'DELETE'])



