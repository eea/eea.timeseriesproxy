cd /var/www/html/temp
find . -name '*.pid' -type f -mmin +1440 -delete
find . -name '*.pdf' -type f -mmin +1440 -delete
find . -name '*.png' -type f -mmin +1440 -delete
find . -name '*.csv' -type f -mmin +1440 -delete
find . -name '*.tif' -type f -mmin +1440 -delete
