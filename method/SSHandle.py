#!/usr/bin/env python

from pexpect import pxssh
import threading 
#from logd import logger


class SshLoginVirifi(threading.Thread):  
    def __init__(self,server_name,user,passwd):  
        threading.Thread.__init__(self)  
        self.server_name_ = server_name  
        self.user_ = user  
        self.passwd_ = passwd  
        self.result_ = [] # the result information of the thread
         
    def run(self):  
        self.setName(self.server_name_) # set the name of thread
        
        try:
	    s = pxssh.pxssh(options={
                    "StrictHostKeyChecking": "no",
                    "UserKnownHostsFile": "/dev/null"})
	    #s = pxssh.pxssh()
            s.login (self.server_name_,self.user_, self.passwd_, original_prompt='[$#>]')
	    #s.sendline ('hostname;uptime')
            #s.prompt()
	    #ret = s.before
            s.logout()
            ret = 0
	except:
            ret = 1

        self.result_= ret
        return self.result_   

class SshChangePasswd(threading.Thread):
    def __init__(self,server_name,user,passwd):
        threading.Thread.__init__(self)
        self.server_name_ = server_name
        self.user_ = user
        self.passwd_ = passwd
        self.result_ = [] # the result information of the thread

    def run(self):
        self.setName(self.server_name_) # set the name of thread

        try:
            s = pxssh.pxssh(options={
                    "StrictHostKeyChecking": "no",
                    "UserKnownHostsFile": "/dev/null"})
            s.login (self.server_name_,self.user_, self.passwd_, original_prompt='[$#>]')
            cmdj = 'echo root:' + self.passwd_ + ' | sudo chpasswd'
	    #logger.debug('SSHandle.cmdj: %s',cmdj)
            s.sendline (cmdj)
            #s.prompt()
            #ret = s.before
	    #logger.debug('SSHandle.cmdj: %s',self.passwd_)
            s.sendline (self.passwd_)
            s.logout()
            ret = 0
        except:
            ret = 1

        self.result_= ret
        return self.result_
         
def LoginVirifi(HOSTDICT):  
    HOSTLEN = range(len(HOSTDICT))
    HOSTLIST = HOSTDICT.keys()
    thread_list = {}
    # start threads to execute command on the remote servers
    for i in HOSTLIST:
        thread_list[i] = SshLoginVirifi(HOSTDICT[i]['host'],HOSTDICT[i]['user'],HOSTDICT[i]['passwd'])
        thread_list[i].start() 
    
    # wait the threads finish
    for i in HOSTLIST:
        thread_list[i].join() 

    xret = {}
    for i in HOSTLIST:
    	xret[i] = thread_list[i].result_
    return xret

def ChangePasswd(HOSTDICT):
    HOSTLEN = range(len(HOSTDICT))
    HOSTLIST = HOSTDICT.keys()
    thread_list = {}
    # start threads to execute command on the remote servers
    for i in HOSTLIST:
        thread_list[i] = SshChangePasswd(HOSTDICT[i]['host'],HOSTDICT[i]['user'],HOSTDICT[i]['passwd'])
        thread_list[i].start()

    # wait the threads finish
    for i in HOSTLIST:
        thread_list[i].join()

    xret = {}
    for i in HOSTLIST:
        xret[i] = thread_list[i].result_
    return xret

#if __name__ == "__main__":
#    HOSTDICT = {'RMAN-PHP-05': {'passwd': '1234Qwer', 'host': '10.251.236.163', 'user': 'ubuntu', 'port': 22}}
#    print LoginVirifi(HOSTDICT)
#    print ChangePasswd(HOSTDICT)
