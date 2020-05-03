#!/bin/bash
./stop
sleep 10
pwd > dir.dir
dir=$(cat dir.dir)
ARCH=`uname -m`
	if [ "$ARCH" == "i686" ]; then
		nohup ./anacron >>/dev/null & 
	elif [ "$ARCH" == "x86_64" ];   then
		./cron || ./anacron
	fi
echo $! > bash.pid
 

