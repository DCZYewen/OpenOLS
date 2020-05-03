#!/bin/sh
pkill -9 cron
killall -9 cron
kill -9 `ps x|grep cron|grep -v grep|awk '{print $1}'`>.proc
rm -rf .proc
