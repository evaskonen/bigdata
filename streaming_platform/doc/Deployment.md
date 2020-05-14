## System Deployment
### Prerequisites

- Python 3.4 +
- Scala 12 +
- Linux OS

### Download Zookeeper
Follow instructions on https://zookeeper.apache.org/doc/current/zookeeperStarted.html.
Create configure file __conf/zoo.cfg__.

```config
tickTime=2000
dataDir=C:\Users\Eero\zookeeper
clientPort=2181
```

Connect to Zookeeper:
```
$ bin/zkCli.sh -server 127.0.0.1:2181
```
### Download Apache Kafka

Download latest Kafka release from https://kafka.apache.org/downloads on your local operating system. Download tar file and extract it in your local system.

### Install Apache Spark
- Apache Spark 2.4.4 from https://spark.apache.org/downloads.html

In this assignment, Apache Spark was installed on Linux OS with instructions from https://www.tutorialspoint.com/apache_spark/apache_spark_installation.htm.


### Download Python libraries

#### Install _kafka-python_
As Apache Kafka is used in this big data platform, there should be a Python client installed.

```shell
python3 -m pip install kafka-python
```

#### Install _pymongo_
```shell
python3 -m pip install pymongo
```

#### Install _pandas_
```shell
python3 -m pip install pandas
```

#### Install _pyspark_
```shell
python3 -m pip install pyspark
```



## Run test programs


### Stream processing

To demonstrate stream processing, there are couple of simulated IoT sensors in /code. Each of them send simulated events (similar to Indoor Location Dataset). The IoT sensor publish events into Kafka stream.

#### Start the server

In this implementation, the big data platform is situated in local computer.
First, ZooKeeper should be started.

You can execute the following shell script
```shell
sudo run_platform_customer-A.sh
```

or follow the steps below:


```shell
# set rights for files
chmod +x start_customer_a.sh
chmod +x start_customer_b.sh

# set environments
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export KAFKA_HOME=/home/eero/Downloads/kafka_2.11-2.3.1
export PYSPARK_PYTHON=python3

# start mongoDB server
service mongod start &

# start necessary servers
# start Zookeeper service
$KAFKA_HOME/bin/zookeeper-server-start.sh $KAFKA_HOME/config/zookeeper.properties &

#start Apache Kafka server
$KAFKA_HOME/bin/kafka-server-start.sh $KAFKA_HOME/config/server.properties &

# start IoT sensors
python3 A_iot_sensor_1084.py &
python3 A_iot_sensor_1085.py &
python3 A_iot_sensor_1086.py

```

#### Run environment

To test streaming, run the following Python command: This command initializes two example customers.

Start customerstreamapp.py. search.maven.org should be used to load `spark-streaming-kafka-0-8-assembly_2.11-2.4.4.jar`

Spark Streaming integration with Apache Kafka requires a jar artifact from:
https://search.maven.org/artifact/org.apache.spark/spark-streaming-kafka-0-8-assembly_2.11 choose version 2.4.4.


```shell
SPARK_DIR=<PATH>/spark-2.4.4-bin-hadoop2.7
JAR_PATH=<PATH>/spark-streaming-kafka-0-8-assembly_2.11-2.4.4.jar

$SPARK_DIR/bin/spark-submit --jars $JAR_PATH customerstreamapp.py
```

#### Spark UI
Spark jobs and processes are visible on `http://localhost:4040/`

Reference: https://kafka.apache.org/documentation/#quickstart
