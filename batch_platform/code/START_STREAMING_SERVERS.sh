#!/bin/sh

# start server processes for MongoDB
mongod &

# start Zookeeper service
./$KAFKA_HOME/bin/windows/zookeeper-server-start.bat config/zookeper.properties &

#start Apache Kafka server
./$KAFKA_HOME/bin/windows/kafka-server-start.bat config/server.properties &

# start simulated IoT sensor
./iot_sensor_1.py &
./iot_sensor_2.py
