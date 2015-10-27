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
from method.definex import *


class BaseHandler(tornado.web.RequestHandler): #BaseHandler
    def get_current_user(self):
        user = self.get_secure_cookie('username')
        return user
 
class WelcomexHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        if not self.current_user:
            self.redirect('/Signin')
            return
        username = self.get_secure_cookie('username')
        permission = permissiondict[username]['permission']
        html_content = ''
        self.render('server_initialization.html',GAMEDICT=gamedict,FLAGID=id,MENUDICT=menudict,PERMISSION=permission,html_content=html_content)

class WelcomeyHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self,id):
        if not self.current_user:
            self.redirect('/Signin')
            return
        username = self.get_secure_cookie('username')
        permission = permissiondict[username]['permission']
     
        content = []
        content.append('<h1>请选择要执行的命令</h1>')
        content.append('''<form method="post" action="/saltresult/''' + id + '''">''')

        # TARGET/ HOST OR GROUP
        content.append('''<p>salt <select name="tgt"> ''')
        for x in gamedict[id]['target']:
          content.append(''' <option value=" ''' + x + '''">''' + x + '''</option>''')
        content.append('''</select>''')
  
        # CMD TYPE/ STATE.SLS OR CMD.RUN 
        content.append(gamedict[id]['cmdtype'])
        
        # CMD0 
        content.append('''<select name="cmd0">''')
        for y in gamedict[id]['cmd0']:
          if gamedict[id]['cmdtype'] == 'cmd.run':
            y_short = y.split('/')[-1]
          else:
            y_short = y
          content.append(''' <option value=" ''' + y + '''">''' + y_short + '''</option>''') 
        content.append('''</select>''')

        # CMD1 
        if gamedict[id].has_key('cmd1'):
          CMD1 = gamedict[id]['cmd1']
          if CMD1[0] == 'textfield':
            content.append('''<input type="text" name="cmd1" style="width:300px"></p>''')
          elif CMD1[0] == 'textarea':
            content.append('''</p><p><textarea name="cmd1" rows="5" cols="60"></textarea></p>''')
          else:
            content.append('''<select name="cmd1">''')
            for z in gamedict[id]['cmd1']:
              content.append(''' <option value=" ''' + z + '''">''' + z + '''</option>''')
            content.append('''</select>''')

        # CMD2 
        if gamedict[id].has_key('cmd2'):
          CMD2 = gamedict[id]['cmd2']
          if CMD2[0] == 'textfield':
            content.append('''<input type="text" name="cmd2" style="width:300px"></p>''')
          elif CMD2[0] == 'textarea':
            content.append('''</p><p><textarea name="cmd2" rows="5" cols="60"></textarea></p>''')
          else:
            content.append('''<select name="cmd2">''')
            for j in gamedict[id]['cmd2']:
              content.append(''' <option value=" ''' + j + '''">''' + j + '''</option>''')
            content.append('''</select>''')

        content.append('''<input type="submit" value="Submit"> </form>''')

	html_content = ' '.join(content)
        self.render('base.html',GAMEDICT=gamedict,FLAGID=id,MENUDICT=menudict,PERMISSION=permission,html_content=html_content)
