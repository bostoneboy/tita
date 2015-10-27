#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
reload(sys)

#from handler.Han import IndexHandler,WelcomexHandler,SigninHandler,SignoutHandler,SaltresultHandler,SingleretHandler
from handler.Ops import *
from handler.SignInOut import *
from handler.SaltResult import *
from handler.HostResult import *

url = [
    (r"/", IndexHandler), #路由设置/ 使用IndexHandler
    (r"/ops/server_initialization", WelcomexHandler),
    (r"/ops/([a-zA-Z_]+)", WelcomeyHandler),
    (r"/Signin", SigninHandler), # Signin使用SigninHandler
    (r"/Signout", SignoutHandler),
    (r"/ChangePW", ChangePWHandler),
    (r"/(ReleaseNotes|Redirect)", RedirectHandler),
    (r"/saltresult/([a-zA-Z_]+)", SaltresultHandler),
    (r"/hostresult/([a-zA-Z_]+)", HostresultHandler),
    (r"/singleret/([a-zA-Z_]+)", SingleretHandler),
    (r"/pageret/([a-zA-Z_]+)", PageretHandler),
]
