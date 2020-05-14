## System Deployment

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

Set a system variable `KAFKA_HOME`
```shell
export KAFKA_HOME=<your_kafka_directory>
```

### Download Python libraries

#### Install _kafka-python_
As Apache Kafka is used in this big data platform, there should be a Python client installed.

```shell
python -m pip install kafka-python
```

#### Install _pymongo_
```shell
python -m pip install pymongo
```

#### Install _pandas_
```shell
python -m pip install pandas
```

#### Install _pyspark_
```shell
python -m pip install pyspark
```



## Run test programs

### Batch processing
__mysimbdp__ contains multiple functions and there are couple of ways to test the performance. After started servers, data ingestion could be tested. To test batch processing feature of this big data platform, please run following command:
```shell
python batchingestmanager.py
```
After started this program, it asks for a data directory and customer ID.
You can use the following values for test customer:
- data directory: `~/assignment-2-478360/data`
- customer ID: `A` or `B`

To demonstrate batch processing, there is a test program:
```shell
./TEST_BATCHINGESTAMANAGER.sh
```
or you can directly run the Python script:
```shell
python batchingestmanager.py
```

### Stream processing

To demonstrate stream processing, there are couple of simulated IoT sensors in /code. Each of them send simulated events (similar to Indoor Location Dataset). The IoT sensor publish events into Kafka stream.



#### Start the server

In this implementation, the big data platform is situated in local computer.
First, ZooKeeper should be started. Please note: Following commands is suitable for Windows OS. If you are using Linux/macOS, please uses `/bin/` instead of `/bin/windows/` and replace `.bat` with `.sh`.
```shell
./bin/windows/zookeeper-server-start.sh config/zookeper.properties
```

Start servers and IoT sensor
```shell
./bin/windows/kafka-server-start.bat config/server.properties
```

```shell
python iot_sensor_1.py
```
```shell
python iot_sensor_2.py
```

```shell
mongod
```

Server can be started with executing shell script in /code folder:
```shell
./START_STREAMING_SERVERS.sh
```

#### Test program for stream processing

To test streaming, run the following Python command: This command initializes two example customers.
```shell
python streamingestmanager.py
```

Reference: https://kafka.apache.org/documentation/#quickstart
