#!/bin/bash

cd dvna && git pull origin master
export MYSQL_USER=root
export MYSQL_DATABASE=dvna
export MYSQL_PASSWORD=AyushPriya#10
export MYSQL_HOST=127.0.0.1
export MYSQL_PORT=3306
npm install
pm2 restart server.js
