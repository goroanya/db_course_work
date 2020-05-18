## Data Base Basics course work

### Documentation:
- [Terms of reference](docs/Технічне_Завдання_Городченко_Анна_КП_72.docx)

### Scaling MongoDB:
Scaling is implemented with MongoDB sharding.
- To run your multiple databases use `sh start_db.sh` script which executes following:
```shell script
# start first shard db instance
mongod --fork --syslog --dbpath data/instance1 --port 27000
# start second shard db instance
mongod --fork --syslog --dbpath data/instance2 --port 27001
# start config db instance
mongod --fork --syslog --configsvr --dbpath data/config --port 27002
# start main db instance which can be used by other applications
mongos --fork --syslog --configdb 127.0.0.1:27002 --port 27100
```
- To connect to main db in mongo shell use `mongo --port 27100`

- To configure sharding (you need to execute this only once) execute in mongo shell:
```shell script
sh.addShard("127.0.0.1:27000")
sh.addShard("127.0.0.1:27001")
use admin
sh.enableSharding("ads")
```
- To add new shard execute in mongo shell:
```shell script
sh.addShard("<mongo db connection string>")
```
- To run sharding operation execute in mongo shell:
```shell script
use admin
db.runCommand({shardCollection: "ads.ads", key: {price: 1}})
```
- To check sharding status execute in mongo shell:
```shell script
db.printShardingStatus()
```

#####Replication instruction:
```shell
#Start the server as PRIMARY (master)
mongod --dbpath /var/lib/mongo/my_database_1 --port 27001 --replSet My_Replica_Set --fork --logpath /var/log/mongodb/my_database_1.log
#Start the server as SECONDARY (slave):
mongod --dbpath /var/lib/mongo/my_database_2 --port 27002 --replSet My_Replica_Set --fork --logpath /var/log/mongodb/my_database_2.log
#Start the server as an arbiter (which does not store data):
mongod --dbpath /var/lib/mongo/my_database_3 --port 27003 --replSet My_Replica_Set --fork --logpath /var/log/mongodb/my_database_3.log
```
PRIMARY server settings:
```shell
mongo --host 127.0.0.1 --port 27001
rs.initiate({"_id" : "My_Replica_Set", members : [ {"_id" : 0, priority : 3, host : "127.0.0.1:27001"}, {"_id" : 1, host : "127.0.0.1:27002"}, {"_id" : 2, host : "127.0.0.1:27003", arbiterOnly : true} ] });
```
As a result, the configured MongoDB will be available at `mongodb://127.0.0.1:27003`.

Author: [Anna Horodchenko](https://t.me/goroanya)