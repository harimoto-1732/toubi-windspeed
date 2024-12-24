#!/bin/bash

head="/var/www/html/wind/data/"
if [ $(date '+%H%M') = '0000' ]; then
    url="http://192.168.62.100/csv_download.php?type=ten_min&date="$(date '+%Y/%m/%d' --date 'yesterday')
    name=$head$(date '+%Y%m%d' --date 'yesterday').csv
else
    url="http://192.168.62.100/csv_download.php?type=ten_min&date="$(date '+%Y/%m/%d')
    name=$head$(date '+%Y%m%d').csv
fi
curl --digest $url -o $name
