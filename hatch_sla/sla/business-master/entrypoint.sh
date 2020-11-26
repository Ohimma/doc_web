#!/bin/bash
function run
{
    #./venv/bin/gunicorn -c gunicorn_conf.py app:app
    gunicorn -c gunicorn_conf.py run:app
}

function stop
{
    kill -9 `ps aux |grep gunicorn |grep treant |awk '{ print $2 }'`
}


if [ "$1" = "run" ]; then
    run
fi

if [ "$1" = "stop" ]; then
    stop
fi

