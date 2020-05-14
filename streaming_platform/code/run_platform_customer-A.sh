#!/bin/sh

# This script start streaming platform

# set environments
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export KAFKA_HOME=/home/eero/Downloads/kafka_2.11-2.3.1
export PYSPARK_PYTHON=python3

# start mongoDB server
#service mongod start &

# start necessary servers
# start Zookeeper service
$KAFKA_HOME/bin/zookeeper-server-start.sh $KAFKA_HOME/config/zookeeper.properties &

#start Apache Kafka server
$KAFKA_HOME/bin/kafka-server-start.sh $KAFKA_HOME/config/server.properties &

sleep 10 &

# start IoT sensors
python3 A_iot_sensor_1084.py &
python3 A_iot_sensor_1085.py &
python3 A_iot_sensor_1086.py &

sleep 10 &

# start Apache Spark with customerstreamapp
export SPARK_DIR=~/spark-2.4.4-bin-hadoop2.7
export JAR_PATH=/home/eero/Downloads/spark-streaming-kafka-0-8-assembly_2.11-2.4.4.jar

$SPARK_DIR/bin/spark-submit --jars $JAR_PATH customerstreamapp.py > spark_log_201911281045.log 2>&1
