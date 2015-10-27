#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
reload(sys)
from method.definex import *
from logd import logger
sys.setdefaultencoding('utf-8')

#userdict = Readyaml('db/user.db')
#logger.debug('Read configuration user.db: %s',userdict)
permissiondict = Readyaml('db/permission.db')
logger.debug('Read configuration permission.db: %s',permissiondict)
gamedict = Readyaml('db/game.db')
logger.debug('Read configuration game.db: %s',gamedict)
menudict = Readyaml('db/menu.db')
logger.debug('Read configuration menu.db: %s',menudict)
