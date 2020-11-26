#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask_bootstrap import Bootstrap
from app import create_app, db

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

bootstrap = Bootstrap(app)

#manager = Manager(app)
#migrate = Migrate(app, db)

if __name__ == '__main__':
    print("app-start")
    #app.run(debug=True) 
    app.run() 

##http://cwiki.guazi.com/pages/viewpage.action?pageId=65932215



