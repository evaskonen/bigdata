#!/bin/sh

# start server processes for MongoDB
#service mongod start &

# start Zookeeper service
$KAFKA_HOME/bin/zookeeper-server-start.sh $KAFKA_HOME/config/zookeeper.properties &

#start Apache Kafka server
$KAFKA_HOME/bin/kafka-server-start.sh $KAFKA_HOME/config/server.properties &
