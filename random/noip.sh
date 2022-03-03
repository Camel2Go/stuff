#!/bin/sh
cd /home/pi/stuff/noip
ip=`curl -s ifconfig.me`
/usr/local/bin/noip2 -i $ip
echo `date +"%d.%m. %T"` "->" $ip>>noip.log
echo $ip >lastip.txt
