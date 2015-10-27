#!/bin/sh

# stop process
kill `ps -ef | grep 'python ops_server_alpha.py' | grep -v grep | awk '{print $2}'`

# start process
cd /data/tornado
/usr/bin/python ops_server_alpha.py &
