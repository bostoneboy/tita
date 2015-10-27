#-*- coding: utf-8 -*-
import logging

class CheloExtendedLogger(logging.Logger):
    """
    Custom logger class with additional levels and methods
    """
    #WARNPFX = logging.WARNING+1
 
    def __init__(self, name):
        logging.Logger.__init__(self, name, logging.DEBUG)               
 
        #logging.addLevelName(self.WARNPFX, 'WARNING')
 
	# 再创建一个handler，用于输出到控制台  
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

	# 创建一个handler，用于写入日志文件
        fh = logging.FileHandler('tornado.log')
        fh.setLevel(logging.DEBUG)

        # create formatter and add it to the handlers
        #formatter = logging.Formatter("%(asctime)s [%(funcName)s: %(filename)s,%(lineno)d] %(message)s")
	formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)
 
        # add the handlers to logger
        self.addHandler(ch)
        self.addHandler(fh)
 
        return
 
    #def warnpfx(self, msg, *args, **kw):
    #    self.log(self.WARNPFX, "! PFXWRN %s" % msg, *args, **kw)
 
 
logging.setLoggerClass(CheloExtendedLogger)   
logger = logging.getLogger("rrcheck")
logger.setLevel(logging.DEBUG)
 
#def test():
#    rrclogger.debug("DEBUG message")
#    rrclogger.info("INFO message")
#    rrclogger.warnpfx("warning with prefix")
# 
#test()

