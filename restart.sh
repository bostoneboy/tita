#!/bin/sh

# stop process
kill `ps -ef | grep 'python index.py' | grep -v grep | awk '{print $2}'`

# start process
cd /data/tornado
/usr/bin/python index.py &
