# -*- coding: utf-8 -*-


cache_config = {
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_HOST': '10.16.208.179',
    'CACHE_REDIS_PORT': 80,
    'CACHE_REDIS_DB': '1',
    'CACHE_REDIS_PASSWORD': '12345'
}

class BaseConfig:  # 基本配置类
    SECRET_KEY = 'Sre'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class TestingConfig(BaseConfig):     #测试环境
    PRESTO_DOMAIN = "presto.guazi-apps.com"
    PRESTO_PORT = 9400
    PRESTO_USER = "tengxuntao"
    PRESTO_GROUP = "presto-sre"
    PRESTO_PASSWORD = "97DFC640CEBEE9874901C9796615AEF1"
    PRESTO_CATALOG = "hive"
    PRESTO_SCHEMA = "sre"
    #PRESTO_CONN = '"presto.guazi-apps.com", port=9400, username=tengxuntao, group=presto-sre, password=97DFC640CEBEE9874901C9796615AEF1, catalog=hive, schema=sre'
    TESTING = True

    CMDB_DOMAIN = "http://c4.guazi-corp.com"
    
    CMDB_DATABASE_URI = "mysql+pymysql://prime_w:t%rAd1@10.16.17.2:3999/cmdb?charset=utf8"
    EARTHWORM_DATABASE_URI = "mysql+pymysql://eathworm_r:xm0CLfiQ9mIt@10.16.17.6:3405/eathworm"
    MEDUSA_DATABASE_URI = "mysql+pymysql://eathworm_r:xm0CLfiQ9mIt@10.16.17.6:3405/saber"

    CACHE_HOST = "10.16.208.179"
    CACHE_PORT = "80"
    CACHE_PASSWORD = "12345"

    NOC_DATABASE_URL = "mysql+pymysql://noc:nocpasswd@10.16.208.178/noc?charset=utf8"

    BIGDATA_DATABASE_URL = "mysql+pymysql://root:root@g1-bdp-test-01.dns.guazi.com/sre?charset=utf8"


    CACHE_DOMAIN = "http://127.0.0.1:5000/"
    #CACHE_DOMAIN = "http://business.guazi-cloud.com/"

class ProductionConfig(BaseConfig):      #生产环境
    TESTING = True
    PRESTO_DOMAIN = "presto.guazi-apps.com"
    PRESTO_PORT = 9400
    PRESTO_USER = "tengxuntao"
    PRESTO_GROUP = "presto-sre"
    PRESTO_PASSWORD = "97DFC640CEBEE9874901C9796615AEF1"
    PRESTO_CATALOG = "hive"
    PRESTO_SCHEMA = "sre"

    CMDB_DOMAIN = "http://c4.guazi-corp.com"

    CMDB_DATABASE_URI = "mysql+pymysql://guazi_cmdb_r:PkD3D(DwRQ9@su^0JC@g1-devops-ku-w.dns.guazi.com:3405/guazi_cmdb?charset=utf8"
    EARTHWORM_DATABASE_URI = "mysql+pymysql://saber_earth_r:F0yyawGudk6xM@g1-devops-ku-w.dns.guazi.com:3405/earthworm"
    MEDUSA_DATABASE_URI = "mysql+pymysql://saber_earth_r:F0yyawGudk6xM@g1-devops-ku-w.dns.guazi.com:3405/saber"

    CACHE_HOST = "10.16.9.99"
    CACHE_PORT = "6379"
    CACHE_PASSWORD = "qwer#123$a"

    CACHE_DOMAIN = "http://business.guazi-corp.com/"

config = {
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': TestingConfig
}
