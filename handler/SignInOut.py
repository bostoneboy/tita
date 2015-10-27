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
from salt.client.ssh.client import SSHClient


from logd import logger
from readConfig import *
reload(readConfig)
from method.definex import *


class BaseHandler(tornado.web.RequestHandler): #BaseHandler
    def get_current_user(self):
        user = self.get_secure_cookie('username')
        return user
 
class IndexHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        if not self.current_user:
            self.redirect('/Signin') #如未登录，则跳转Signin，Signin的GET方法调用的就是login_form.html页面
            return
	id = 'server_initialization'
	username = self.get_secure_cookie('username')
	permission = permissiondict[username]['permission']
        if 'All' in permission or '服务器' in permission: 
          self.render('index.html',GAMEDICT=gamedict,FLAGID=id,MENUDICT=menudict,PERMISSION=permission)
        else:
          for n in menudict:
            if menudict[n].has_key(permission[0]):
              uri = menudict[n][permission[0]].values()[0]
              uri = '/ops/' + uri
              break
          self.redirect(uri)

class RedirectHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self,id):
        if not self.current_user:
            self.redirect('/Signin')
            return
        uri = id + '.html'
        self.render(uri)


class SigninHandler(BaseHandler): #引入BaseHandler
    def post(self): #HTTP的POST方法，是GET渲染的form中的post method所对应
        username = self.get_argument('username')	#获取form中username的值
        password = self.get_argument('password')	#获取form中password的值
        ip = self.request.remote_ip #获取来访者IP
	try: 
            userdict = Readyaml('db/user.db')
            wdsalt = userdict[username]['salt']
            wdpass = userdict[username]['password']
            wdforcereset = userdict[username]['forcereset']
            wdret = VerifyPassword(wdsalt,wdpass,password)
	    if wdret == 0:
		permission = permissiondict[username]['permission']
                self.set_secure_cookie('username', username.encode('unicode_escape'),  expires_days=None) #same
                self.set_secure_cookie('role', password.encode('unicode_escape'),  expires_days=None) #same
                ip = self.request.remote_ip #获取来访者IP
		logger.debug('User %s auth success',username)

                if wdforcereset == 1:
		    logger.debug('User %s is forced to change password',username)
                    self.redirect('/ChangePW')
                else:
                    self.redirect('/') 
                return #返回，按照官方文档的要求，在redirect之后需要写空的return，否则可能会有问题，实测确实会有问题
	    else:
		logger.debug('User %s login failed, wrong password',username)
	        self.redirect('/Signin') #跳转回登录页面
                return
	except:
	    logger.debug('User %s login failed, wrong username',username)
	    self.redirect('/Signin')
            return
    def get(self): #HTTP GET方式
        self.render('login_form.html') #渲染登录框HTML

class SignoutHandler(BaseHandler):  
    def get(self):  
	username = self.get_secure_cookie('username')
        if (self.get_argument("signout", None)):  
            self.clear_cookie("username")  
	logger.debug('User %s logout',username)
        self.redirect("/") 

class ChangePWHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        if not self.current_user:
            self.redirect('/Signin')
            return
	userdict = Readyaml('db/user.db')
        username = self.get_secure_cookie('username')
	password0 = self.get_argument('password0')
	password1 = self.get_argument('password1')
  	if password0 == password1:
	    salt = RandomString(64)
 	    password = GenDigest(salt,password0)
            userdict[username]['salt'] = salt
            userdict[username]['password'] = password
            userdict[username]['forcereset'] = 0
	    logger.debug('Modify userdict: %s',userdict)
            Writeyaml(userdict,'db/user.db')
 	    self.redirect("/Redirect")
            
    def get(self): #HTTP GET方式
        self.render('change_passwd.html')
