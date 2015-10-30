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
 
class SaltresultHandler(BaseHandler): #引入BaseHandler
    def post(self,id):
        username = self.get_secure_cookie('username')
        permission = permissiondict[username]['permission']
	global SALTRET
	SALTRET = 'Just init value'

        TARGET = self.get_argument('tgt')     
        FUN = gamedict[id]['cmdtype']
        EXPR_FORM = gamedict[id]['targettype']
        RUNAS = gamedict[id]['runas']
        if RUNAS == 'na':
          KWARG = {}
        else:
          KWARG = {'runas':RUNAS}
        CMD0 = self.get_argument('cmd0')
        CMD1 = self.get_argument('cmd1')
        try:
          CMD2 = self.get_argument('cmd2')
        except:
          CMD2 = ''
        if FUN == 'cmd.run':
          COMMAND = ' '.join([CMD0,CMD1,CMD2])
        elif FUN == 'state.sls':
          COMMAND = CMD0 + '.' + CMD1 + CMD2
        if EXPR_FORM == 'list':
          SALTCMD = "salt %s %s %s" % (TARGET,FUN,COMMAND)
        elif EXPR_FORM == 'nodegroup':
          SALTCMD = "salt -N %s %s %s" % (TARGET,FUN,COMMAND)

        local = salt.client.LocalClient()
        self.render('result.html',SALTCOMMAND=SALTCMD,SALTRESULT=SALTRET,FLAGID=id,MENUDICT=menudict,SALTFUNCTION=FUN,PERMISSION=permission)
        logger.debug('%s, salt.client.local.cmd: tgt=%s,fun=%s,arg=[%s],expr_form=%s,kwarg=%s',username,TARGET,FUN,COMMAND,EXPR_FORM,KWARG)
        SALTRET = local.cmd(tgt=TARGET,fun=FUN,arg=[COMMAND],expr_form=EXPR_FORM,kwarg=KWARG)
        logger.debug('%s, SALTRET0: %s',username,SALTRET)
        if FUN == 'state.sls':
          SALTRET = ret_process(SALTRET)
        logger.debug('%s, SALTRET: %s',username,SALTRET)
            

class SingleretHandler(SaltresultHandler):
    @tornado.web.authenticated
    def get(self,id):
        if not self.current_user:
            self.redirect('/Signin')
            return
        username = self.get_secure_cookie('username')
        permission = permissiondict[username]['permission']
        PAGE = ''.join([id,'.html'])
        logger.debug('%s, SALTRESULT: ',username)
        logger.debug('Request %s',PAGE)
        self.render(PAGE,SALTRESULT=SALTRET )

