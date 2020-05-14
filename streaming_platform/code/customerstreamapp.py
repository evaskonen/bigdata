import sys
import os

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from kafka import KafkaConsumer, KafkaProducer
from pyspark.streaming.kafka import KafkaUtils
from mysimbdp import databroker
import json
#import pandas as pd

def createStreamingContext(list_of_topics, window_size, numPartitions=None):
    '''
    Get data stream from Kafka broker
    '''

    # Spark context
    #sc = SparkContext(appName="PythonSparkStreamingKafka")
    sc = SparkContext(appName="PythonStreamingDirectKafka")
    # sc.setLogLevel("WARN")

    # Streaming context
    batch_duration = 6 # batch duration in seconds
    ssc = StreamingContext(sc,batch_duration)

    # Connect to Kafka and get DStream of input stream data
    kafkaStream = KafkaUtils.createDirectStream(ssc, list_of_topics, {"metadata.broker.list": "localhost:9092"})

    # windowed stream
    windowedStream = kafkaStream.window(window_size)

    # messages should be in JSON format
    #DStream = kafkaStream.map(lambda x: json.loads(x[1]))
    DStream = windowedStream.map(lambda x: eventJSON(x[1])).filter(lambda x: len(x) > 0)
    #lines = windowedStream.map(lambda x: x[1])
    # https://github.com/apache/spark/blob/v2.4.4/examples/src/main/python/streaming/sql_network_wordcount.py
    #test
    if numPartitions:
        try:
            DStream.repartition(numPartitions)
        except Exception:
            pass
    DStream.pprint()

    # after streaming context and operations are defined, it is time to start streaming process
    ssc.start()
    ssc.awaitTermination()
    #startStreaming(stc)

    return DStream

def eventJSON(message):
    '''
    Function to load json format messages. Return an JSON object or empty string in a case of non-JSON message.
    '''
    # Reference: https://community.cloudera.com/t5/Support-Questions/How-to-parse-Streaming-Json-object/td-p/139577
    try:
        return json.loads(message)
    except Exception:
        return {}

def countEvents():
    '''
    Count streaming events by key
    '''

def startStreaming(streamingContext):
    '''
    This function starts a Spark streaming
    '''
    # Start the streaming context
    streamingContext.start()
    streamingContext.awaitTermination()

def parseSensorData(spark):
    sensorDF = spark.sql("SELECT part_id, ts_time, ts_date, room")
    pass

def sendEventBroker(event, topic):
    '''
    This function sends a Spark batch into the Kafka broker
    '''
    databroker(event, topic)

def window(kafkaStream, window_size):
    return kafkaStream.window(window_size)

if __name__ == "__main__":
    print('Welcome to customerstreamapp!\n')
    print('-----------------------------')
    customer = 'A'
    #customer = str(sys.argv[0])

    if customer == 'B':
        list_of_topics = ['0001', '0002', '0003', '0004']
        window_size = 43200000
    elif customer == 'A':
        list_of_topics = ['1084', '1085', '1086']
        window_size = 86400000
    stream = createStreamingContext(list_of_topics, window_size)
    print(stream)
