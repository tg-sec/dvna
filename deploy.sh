#!/bin/bash

cd dvna && git pull origin master
pm2 stop server.js
export MYSQL_USER=root
export MYSQL_DATABASE=dvna
export MYSQL_PASSWORD=<db password>
export MYSQL_HOST=localhost
export MYSQL_PORT=3306
pm2 start server.js
