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

from definex import *

username = sys.argv[1]
password = RandomString(8)
salt 	 = RandomString(64)

passwordx = GenDigest(salt,password)
forcereset = 1

userdict = Readyaml('../db/user.db')

dictx = {}
dictx['salt'] = salt
dictx['password'] = passwordx
dictx['forcereset'] = forcereset
userdict[username] = dictx

Writeyaml(userdict,'../db/user.db')

#print('userdict: %s\n' % userdict)
print('New user added success:\nUsername: %s\nPassword: %s' % (username,password))
