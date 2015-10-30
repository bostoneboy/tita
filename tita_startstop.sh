#!/bin/sh
## 进程重启脚本
## 接受的操作 stop,start,restart

USAGE () {
  echo "USAGE:
  $0 start|stop|restart"
  echo ""
  exit 1
}

if [ $# -ne 1 ]
then
  USAGE
fi

stop_proc() {
  kill `ps -ef | grep 'python ops_server_alpha.py' | grep -v grep | awk '{print $2}'`
  proc_count=`ps -ef | grep -v grep | grep -c 'python ops_server_alpha.py'`
  if [ "${proc_count}" -eq 0 ]
  then
    echo "Success! Process stoped."
  else
    echo "Error! Process stop failed."
    exit 2
  fi
}

start_proc() {
  /usr/bin/python ops_server_alpha.py &
  proc_count=`ps -ef | grep -v grep | grep -c 'python ops_server_alpha.py'`
  if [ "${proc_count}" -gt 0 ]
  then
    echo "Success! Process started."
  else
    echo "Error! Process stop failed."
  fi
}

FLAG=$1
case "x${FLAG}" in
xstop)
  stop_proc
  ;;
xstart)
  start_proc
  ;;
xrestart)
  stop_proc
  sleep 1
  start_proc
  ;;
*)
  USAGE
  ;;
esac

