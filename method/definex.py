#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import yaml
import json
import time
import os
import random
import string

from hashlib import sha256


def Readict(filenamex):
        of = open(filenamex,'r')
        readlist = readfile.readlines()
        of.close()
        readdict = {}
        for k in range(len(readlist)):
            readdict[k] = readlist[k].split()
        return readdict

def Readyaml(filenamex):
        of = open(filenamex,'r')
        dictx = yaml.load(of)
        of.close()
        return dictx

def Writeyaml(dictx,filenamex):
        of = open(filenamex,'w')
        of.write(yaml.dump(dictx,default_flow_style=False))
        of.close()

def ret_process(RET,dtype='reg'):
  SALTRET = {}
  for i in RET:
    if len(RET[i]) == 0:
      SALTRET[i] = {'result':'NA'}
    else:
      if dtype == 'init':
        TASKX = RET[i]['return']
      else:
        TASKX = RET[i]
      for j in TASKX:
        iresult = TASKX[j]['result']
        if iresult:
          fresult = True
        else:
          fresult = False
          break

      if fresult:
        SALTRET[i] = {'result':True}
      else:
        DETAIL = json.dumps(RET[i],indent=1)
        SALTRET[i] = {'result':False,'detail':DETAIL}
  return SALTRET

def VerifyPassword(salt,passwd,inputpasswd):
    passtring = salt + inputpasswd
    passret = sha256(passtring).hexdigest()
    if passret == passwd:
        return 0
    else:
        return 1

def GenDigest(salt,passwd):
    passtring = salt + passwd 
    return sha256(passtring).hexdigest()

def RandomString(Length):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(Length))
