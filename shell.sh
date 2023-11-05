ntpdate cn.pool.ntp.org

--------------------kerberos------------------------
 /usr/sbin/kdb5_util create -s -r HADOOP.COM
 /usr/sbin/kadmin.local -q "addprinc admin/admin"


cd /var/kerberos/krb5kdc/

kadmin.local -q "addprinc -randkey atttx/slave1@HADOOP.COM"
kadmin.local -q "addprinc -randkey atttx/slave2@HADOOP.COM"
kadmin.local -q "addprinc -randkey atttx/master@HADOOP.COM"

kadmin.local -q "xst -k user.keytab  atttx/slave1@HADOOP.COM"
kadmin.local -q "xst -k user.keytab  atttx/slave2@HADOOP.COM"
kadmin.local -q "xst -k user.keytab  atttx/master@HADOOP.COM"

scp user.keytab slave1:/home/atttx/bigdata/zookeeper/conf
scp user.keytab slave2:/home/atttx/bigdata/zookeeper/conf
scp user.keytab master:/home/atttx/bigdata/zookeeper/conf


ssh slave1 "cd /home/atttx/bigdata/zookeeper/conf/;chown atttx:atttx user.keytab ;chmod 400 *.keytab"
ssh slave2 "cd /home/atttx/bigdata/zookeeper/conf/;chown atttx:atttx user.keytab ;chmod 400 *.keytab"
ssh master "cd /home/atttx/bigdata/zookeeper/conf/;chown atttx:atttx user.keytab ;chmod 400 *.keytab"


delete_principal


---------------------mongodb--------------------------------

yum install cyrus-sasl cyrus-sasl-gssapi cyrus-sasl-plain krb5-libs libcurl libpcap lm_sensors-libs net-snmp net-snmp-agent-libs openldap openssl rpm-libs tcp_wrappers-libs


mkdir -p /home/atttx/bigdata/mongoDB/conf
mkdir -p /home/atttx/bigdata/mongoDB/mongos/log
mkdir -p /home/atttx/bigdata/mongoDB/config/data
mkdir -p /home/atttx/bigdata/mongoDB/config/log
mkdir -p /home/atttx/bigdata/mongoDB/shard1/data
mkdir -p /home/atttx/bigdata/mongoDB/shard1/log
mkdir -p /home/atttx/bigdata/mongoDB/shard2/data
mkdir -p /home/atttx/bigdata/mongoDB/shard2/log
mkdir -p /home/atttx/bigdata/mongoDB/shard3/data
mkdir -p /home/atttx/bigdata/mongoDB/shard3/log



pidfilepath = /home/atttx/bigdata/mongoDB/config/log/configsrv.pid
dbpath = /home/atttx/bigdata/mongoDB/config/data
logpath = /home/atttx/bigdata/mongoDB/config/log/congigsrv.log
logappend = true
 
bind_ip = 0.0.0.0
port = 21000
fork = true
 
#declare this is a config db of a cluster;
configsvr = true

#副本集名称
replSet=configs
 
#设置最大连接数
maxConns=20000


mongod -f /home/atttx/bigdata/mongoDB/conf/config.conf

mongo --port 21000

config = {
 _id : "configs",
 members : [
{_id : 0, host : "192.168.6.128:21000" },
{_id : 1, host : "192.168.6.129:21000" },
{_id : 2, host : "192.168.6.130:21000" }
]
}

vim /home/atttx/bigdata/mongoDB/conf/shard1.conf


#配置文件内容
#——————————————–
pidfilepath = /home/atttx/bigdata/mongoDB/shard1/log/shard1.pid
dbpath = /home/atttx/bigdata/mongoDB/shard1/data
logpath = /home/atttx/bigdata/mongoDB/shard1/log/shard1.log
logappend = true

bind_ip = 0.0.0.0
port = 27001
fork = true
 
#打开web监控
#httpinterface=true
#rest=true
 
#副本集名称
replSet=shard1
 
#declare this is a shard db of a cluster;
shardsvr = true
 
#设置最大连接数
maxConns=20000


mongod -f /home/atttx/bigdata/mongoDB/conf/shard1.conf

mongo --port 27001
#使用admin数据库
use admin
#定义副本集配置，第三个节点的 "arbiterOnly":true 代表其为仲裁节点。
config = {
_id : "shard1",
members : [
{_id : 0, host : "192.168.6.128:27001"},
{_id : 1, host : "192.168.6.129:27001"},
{_id : 2, host : "192.168.6.130:27001", arbiterOnly: true}
]
}
rs.initiate(config)

vi /home/atttx/bigdata/mongoDB/conf/shard2.conf

#配置文件内容
#——————————————–
pidfilepath = /home/atttx/bigdata/mongoDB/shard2/log/shard2.pid
dbpath = /home/atttx/bigdata/mongoDB/shard2/data
logpath = /home/atttx/bigdata/mongoDB/shard2/log/shard2.log
logappend = true

bind_ip = 0.0.0.0
port = 27002
fork = true
 
#打开web监控
#httpinterface=true
#rest=true
 
#副本集名称
replSet=shard2
 
#declare this is a shard db of a cluster;
shardsvr = true
 
#设置最大连接数
maxConns=20000



mongod -f /home/atttx/bigdata/mongoDB/conf/shard2.conf


mongo --port 27002
#使用admin数据库
use admin
#定义副本集配置
config = {
_id : "shard2",
members : [
{_id : 0, host : "192.168.6.128:27002"  , arbiterOnly: true },
{_id : 1, host : "192.168.6.129:27002" },
{_id : 2, host : "192.168.6.130:27002" }
]
}

#初始化副本集配置
rs.initiate(config)


vi /home/atttx/bigdata/mongoDB/conf/shard3.conf

#配置文件内容
#——————————————–
pidfilepath = /home/atttx/bigdata/mongoDB/shard3/log/shard3.pid
dbpath = /home/atttx/bigdata/mongoDB/shard3/data
logpath = /home/atttx/bigdata/mongoDB/shard3/log/shard3.log
logappend = true

bind_ip = 0.0.0.0
port = 27003
fork = true
 
#副本集名称
replSet=shard3
 
#declare this is a shard db of a cluster;
shardsvr = true
 
#设置最大连接数
maxConns=20000


mongod -f /home/atttx/bigdata/mongoDB/conf/shard3.conf


mongo --port 27003
#使用admin数据库
use admin
#定义副本集配置
config = {
_id : "shard3",
members : [
{_id : 0, host : "192.168.6.128:27003" },
{_id : 1, host : "192.168.6.129:27003" , arbiterOnly: true},
{_id : 2, host : "192.168.6.130:27003" }
]
}

#初始化副本集配置
rs.initiate(config)


vi /home/atttx/bigdata/mongoDB/conf/mongos.conf

#内容
pidfilepath = /home/atttx/bigdata/mongoDB/mongos/log/mongos.pid
logpath = /home/atttx/bigdata/mongoDB/mongos/log/mongos.log
logappend = true

bind_ip = 0.0.0.0
port = 20000
fork = true

#监听的配置服务器,只能有1个或者3个 configs为配置服务器的副本集名字
configdb = configs/192.168.6.128:21000,192.168.6.129:21000,192.168.6.130:21000
 
#设置最大连接数
maxConns=20000


mongos -f /home/atttx/bigdata/mongoDB/conf/mongos.conf

mongo --port 20000
#使用admin数据库
use  admin
#串联路由服务器与分配副本集
sh.addShard("shard1/192.168.6.128:27001,192.168.6.129:27001,192.168.6.130:27001")
sh.addShard("shard2/192.168.6.128:27002,192.168.6.129:27002,192.168.6.130:27002")
sh.addShard("shard3/192.168.6.128:27003,192.168.6.129:27003,192.168.6.130:27003")
#查看集群状态
sh.status()



#指定testdb分片生效
db.runCommand( { enablesharding :"testdb"});
#指定数据库里需要分片的集合和片键
db.runCommand( { shardcollection : "testdb.table1",key : {id: 1} } )

mongo  127.0.0.1:20000
#使用testdb
use  testdb;
#插入测试数据
for (var i = 1; i <= 100000; i++)
db.table1.save({id:i,"test1":"testval1"});
#查看分片情况如下，部分无关信息省掉了
db.table1.stats();

{
        "sharded" : true,
        "ns" : "testdb.table1",
        "count" : 100000,
        "numExtents" : 13,
        "size" : 5600000,
        "storageSize" : 22372352,
        "totalIndexSize" : 6213760,
        "indexSizes" : {
                "_id_" : 3335808,
                "id_1" : 2877952
        },
        "avgObjSize" : 56,
        "nindexes" : 2,
        "nchunks" : 3,
        "shards" : {
                "shard1" : {
                        "ns" : "testdb.table1",
                        "count" : 42183,
                        "size" : 0,
                        ...
                        "ok" : 1
                },
                "shard2" : {
                        "ns" : "testdb.table1",
                        "count" : 38937,
                        "size" : 2180472,
                        ...
                        "ok" : 1
                },
                "shard3" : {
                        "ns" : "testdb.table1",
                        "count" :18880,
                        "size" : 3419528,
                        ...
                        "ok" : 1
                }
        },
        "ok" : 1
}


mongodb的启动顺序是，先启动配置服务器，在启动分片，最后启动mongos.

mongod -f /home/atttx/bigdata/mongoDB/conf/config.conf
mongod -f /home/atttx/bigdata/mongoDB/conf/shard1.conf
mongod -f /home/atttx/bigdata/mongoDB/conf/shard2.conf
mongod -f /home/atttx/bigdata/mongoDB/conf/shard3.conf
mongod -f /home/atttx/bigdata/mongoDB/conf/mongos.conf
关闭时，直接killall杀掉所有进程

killall mongod
killall mongos