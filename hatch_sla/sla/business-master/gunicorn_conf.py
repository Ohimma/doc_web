bind = '0.0.0.0:5000'
backlog = 20

workers = 3
worker_class = 'sync'
worker_connections = 1000
timeout = 300000
keepalive = 2

spew = False
#daemon = True
pidfile = 'logs/gunicorn.pid'
#umask = 0
#user = None
#group = None
#tmp_upload_dir = None


#accesslog = 'logs/access.log'
#errorlog = 'logs/error.log'
#loglevel = 'warning'
accesslog = '-'
errorlog = '-'
loglevel = 'info'
access_log_format = '%(h)s %(u)s %(t)s %(r)s %(s)s %(b)s %(f)s %(a)s %(L)ss'

proc_name = 'cmdb'



