#?/bin/bash

mongod --fork --syslog --dbpath data/instance1 --port 27000
mongod --fork --syslog --dbpath data/instance2 --port 27001
mongod --fork --syslog --configsvr --dbpath data/config --port 27002
mongos --fork --syslog --configdb 127.0.0.1:27002 --port 27100
