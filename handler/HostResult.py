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
from method.SSHandle import *


from logd import logger
from readConfig import *
from method.definex import *


class BaseHandler(tornado.web.RequestHandler): #BaseHandler
    def get_current_user(self):
        user = self.get_secure_cookie('username')
        return user
 
class HostresultHandler(BaseHandler): #引入BaseHandler
    def post(self,id):
        username = self.get_secure_cookie('username')
        permission = permissiondict[username]['permission']
	global SALTRET
	global ecount
	SALTRET = 'Just init value'

        if id == 'server_initialization':
          PACKAGE = self.get_argument('package')
	  PACKAGE_LINE = [i.split() for i in PACKAGE.encode('utf-8').split('\r\n')]
	  logger.debug('%s, PACKAGE_LINE: %s',username,PACKAGE_LINE)
    	  SALTCMD = 'Host Initialization'
	  SALT_FUN = 'host.init'

	  ecount = 0
	  SALTRET = []
	  SALTRET.append('')
	  ## 需要加入主机名和IP地址不重复验证
	  ## 日后再加
	  for ELMENT in PACKAGE_LINE:
	    j = ' '.join(ELMENT)
	    if len(ELMENT) < 2:
	      ecount += 1
	      SALTRET.append({j:1})
	    else:
	      SALTRET.append({j:0})
	  logger.debug('%s, ecount: %s SALTRET: %s',username,ecount,SALTRET)
	  if ecount > 0:
	     SALTRET[0] = '下列标红的行所提供之信息不完整，请修正后重新提交: '
	     self.render('result.html',SALTCOMMAND=SALTCMD,ECOUNT=ecount,SALTRESULT=SALTRET,FLAGID=id,MENUDICT=menudict,SALTFUNCTION=SALT_FUN,PERMISSION=permission)

	  else:
	    ret_usertype = 0
	    PACKAGE_DICT = {}
	    HOSTNAME_DICT = {}
	    ROSTER_CONF = '.roster_' + str(time.time())
	    for USER in ['root','ubuntu']:
	      if USER == 'root':
	          for ELMENT in PACKAGE_LINE:
	            if len(ELMENT) == 3:
	              PASS = ELMENT[-1]
	            else:
	              PASS = '1234Qwer'
	            PACKAGE_DICT[ELMENT[1]] = {'host': ELMENT[0],'user':USER,'passwd':PASS,'port':22}
	            HOSTNAME_DICT[ELMENT[0]] = ELMENT[1]
	            PACKAGE_YAML = yaml.dump(PACKAGE_DICT)
                    logger.debug('%s, PACKAGE_YAML: %s',username,PACKAGE_YAML)
	            ROSTER_FD = open(ROSTER_CONF,'w')
	            ROSTER_FD.write(PACKAGE_YAML)
	            ROSTER_FD.close()
	      elif USER == 'ubuntu':
	          for hosty in retb:
	            if retb[hosty] == 0:
		      PACKAGE_DICT.pop(hosty) 
	            elif retb[hosty] == 1:
		      PACKAGE_DICT[hosty]['user'] = 'ubuntu'
	        
	
              logger.debug('%s, PACKAGE_DICT: %s',username,PACKAGE_DICT)
	      TARGET = ','.join([i for i in HOSTNAME_DICT.values()])

	      ## 验证ssh的用户密码是否正确
	      SALTSSH_RETFILE = '.saltsshret_' + str(time.time())

	      retb = LoginVirifi(PACKAGE_DICT) 
	      logger.debug('%s, The result of LoginVirifi: %s',username,retb)
	      retc = sum(retb.values())
	      if retc == 0:
	          ret_usertype = ret_usertype - 1
	          logger.debug('%s, All host LoginVirifi success,ret_usertype: %s',username,ret_usertype)
	          break 
	      else:
	          ret_usertype = 1
	          logger.debug('%s, All or part of host LoginVirifi fail,ret_usertype: %s',username,ret_usertype)
	          continue

	    ## 验证用户为ubuntu时，修改root密码与ubuntu用户密码相同
	    ## ubuntu 用户修改root 密码失败暂未做处理   
	    if ret_usertype == 1:
              ecount = -1
	      SALTRET = []
	      SALTRET.append('下列标红的服务器ssh登录失败，请修正后重新提交：')
	      for j in  PACKAGE_LINE:
	         k = ' '.join(j)
	         if j[1] in retb.keys():
	            SALTRET.append({k:1})
	         else:
		    SALTRET.append({k:0})
              logger.info('%s, ecount: %s SALTRET: %s',username,ecount,SALTRET)
	      self.render('result.html',SALTCOMMAND=SALTCMD,ECOUNT=ecount,SALTRESULT=SALTRET,FLAGID=id,MENUDICT=menudict,SALTFUNCTION=SALT_FUN,PERMISSION=permission)
	    else:
	      #SALT_FUN = 'state.sls'
              self.render('result.html',SALTCOMMAND=SALTCMD,ECOUNT=ecount,SALTRESULT=SALTRET,FLAGID=id,MENUDICT=menudict,SALTFUNCTION=SALT_FUN,PERMISSION=permission)

	      ## 验证用户为ubuntu时，修改root密码与ubuntu用户密码相同
	      ## ubuntu 用户修改root 密码失败暂未做处理   
	      if ret_usertype == 0:
	        retd = ChangePasswd(PACKAGE_DICT)
	        logger.debug('%s, The result of ChangePasswd: %s',username,retd)
	        rete = sum(retd.values())

    	      ## host init
    	      client = SSHClient()
              logger.debug("%s, client.cmd\(tgt=%s,fun='state.sls', arg=['inithost'],roster_file=%s,expr_form=\'list\',kwarg={'pillar':%s,}\)",username,TARGET,ROSTER_CONF,HOSTNAME_DICT)
    	      RET = client.cmd(tgt=TARGET,fun='state.sls', arg=['inithost'],roster_file=ROSTER_CONF,expr_form='list',ignore_host_keys=True,kwarg={'pillar':HOSTNAME_DICT})
	      logger.debug('%s, ecount: %d RET: %s',username,ecount,RET)
    	      #SALTRET = {}
              SALTRET = ret_process(RET,dtype='init')
              logger.info('%s, SALTRET: %s',username,SALTRET)
    	      #for elment in RET:
    	      #  SALTRET[elment] = json.dumps(RET[elment],indent=1)

class PageretHandler(HostresultHandler):
    @tornado.web.authenticated
    def get(self,id):
        if not self.current_user:
            self.redirect('/Signin')
            return
        username = self.get_secure_cookie('username')
        permission = permissiondict[username]['permission']
        PAGE = ''.join([id,'.html'])
        logger.debug('Request %s',PAGE)
        self.render(PAGE,ECOUNT=ecount,SALTRESULT=SALTRET)
