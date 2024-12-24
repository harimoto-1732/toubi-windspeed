#!/bin/sh

fname=$(date +%Y%m%d%H%M)
if [ ${fname:11:1} = '0' ]; then
	convert -geometry 480x360 /var/www/html/pic/cam.jpg /var/www/html/wind/pic/cam.jpg
	cp /var/www/html/wind/pic/cam.jpg /var/www/html/wind/pic/$fname.jpg
else
	convert -geometry 480x360 /var/www/html/pic/cam.jpg /var/www/html/wind/pic/cam.jpg
fi
