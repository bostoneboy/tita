#!/usr/bin/env python
#-*- coding: utf-8 -*-
 
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.autoreload
import yaml
import json
import logging
import time
import os

import salt.client
import ConfigParser
from salt.client.ssh.client import SSHClient
from logd import logger
from url import url

settings = \
    {
        "cookie_secret": "HeavyMetalWillNeverDie", #Cookie secret
        "xsrf_cookies": False, 		#开启跨域安全
        "gzip": False,
        "debug": True,
        "template_path": os.path.join(os.path.dirname(__file__), "./templates"), 
        "static_path": os.path.join(os.path.dirname(__file__), "./static"), 
        "login_url": "/Signin", 
    }


application = tornado.web.Application(
    handlers=url,
    **settings
    )

if __name__ == "__main__": 
#启动tornado，配置里如果打开debug，则可以使用autoload，属于development模式
#如果关闭debug，则不可以使用autoload，属于production模式
#autoload的含义是当tornado监测到有任何文件发生变化，不需要重启server即可看到相应的页Ã§¹浠裨蚴切薷牧硕骺床坏奖浠??

    try:
        port = sys.argv[1]  
    except:
        port = 83    #default server port
    logger.info('Server start at port %s ',port)

    server = tornado.httpserver.HTTPServer(application)
    server.bind(port)              
    server.start() 
    tornado.ioloop.IOLoop.instance().start()
