#!/bin/sh

# IP=`/sbin/ifconfig  | grep 'inet addr:'| grep -v '127.0.0.1' |  cut -d: -f2 | awk '{ print $1}'` # linux
BASE_DIR=` cd "$(dirname "$0")"; cd ..;  pwd `

PROCESS_NAME=${BASE_DIR##*/}
CONFIG_PATH=$BASE_DIR/script/gunicorn_config.py
PID_FILE=$BASE_DIR/script/gunicorn.pid
CMD="gunicorn --daemon -c $CONFIG_PATH app:g_app "

function start_gunicorn() {
    cd $BASE_DIR
    $CMD
    echo "$PROCESS_NAME is running."
}

function stop_gunicorn() {
    if [ -f $PID_FILE ]; then
        PID=`cat $PID_FILE`
        echo "gunicorn: kill PID=${PID}"
        kill -TERM ${PID}
    else
        echo "gunicorn: $PID_FILE not exists..."
    fi
}

function reload_gunicorn() {
    if [ -f $PID_FILE ]; then
        PID=`cat $PID_FILE`
        kill -HUP $PID
        echo "$PID reloaded..."
    else
        echo "$PID_FILE not exists..."
    fi
}

function restart_gunicorn () {
    stop_gunicorn
    sleep 1
    start_gunicorn
}

case "$1" in
    start)
        start_gunicorn
        exit $?
        ;;
    stop)
        stop_gunicorn
        exit $?
        ;;
    restart)
        restart_gunicorn
        exit $?
        ;;
    reload)
        reload_gunicorn
        exit $?
        ;;
    *)
        echo "Usage: $0 { start | stop | restart | reload }"
        exit 1
        ;;
esac