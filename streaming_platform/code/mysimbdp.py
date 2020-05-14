import json
import os
from os import listdir
from kafka import KafkaConsumer, KafkaProducer
#from pandas import DataFrame
#import pandas as pd
from datetime import datetime
from pymongo import MongoClient
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

def streaming_data(topic_name, window_size):
    '''
    Get data stream from Kafka broker
    '''

    # Spark context
    sc = SparkContext(appName="PythonSparkStreamingKafka")
    # sc.setLogLevel("WARN")

    # Streaming context
    batch_duration = 60 # batch duration in seconds
    stc = StreamingContext(sc,batch_duration)

    # Connect to Kafka and get DStream of input stream data
    kafkaStream = KafkaUtils.createStream(stc, 'localhost:2181', 'raw-event-streaming-consumer', {topic_name:1})

    # windowed stream
    windowedStream = kafkaStream.window(window_size)
    # Start the streaming context
    stc.start()
    stc.awaitTermination()

def databroker(message, topic_name):
    '''
    This method implements the mysimbdp-databroker.
    Data should be in a list where each message is in
    json format {'key': 'value'}
    '''
    # Set JSON as a message format
    producer = KafkaProducer(value_serializer=lambda m: json.dumps(m).encode('ascii'))
    topic_name = topic_name
    producer.send(topic_name, message)
    producer.flush()

def insert_coredms(database_name, message):
    '''
    This method inserts a message into the final sink (coredms)
    '''
    client = MongoClient('localhost', 27017)
    database = client[database_name]
    column = database['records']
    column.insert_one(message)
    print('Inserted message: ' + str(message))

def subscribe_stream(topic_name):
    '''
    This method return a Kafka consumer instance
    '''
    return KafkaConsumer(topic_name, value_deserializer=lambda m: json.loads(m.decode('ascii')))

def insert_files(database_name, files):
    '''
    This method inserts a file into the final sink (coredms)
    '''
    client = MongoClient('localhost', 27017)
    # ASSUME CUSTOMER IS PUSHING DATA IN CSV FORMAT

    database = client[database_name]
    column = database["records"]
    # convert pandas DataFrame into dictionary format
    files_json = files.to_dict(orient="records")

    #insert file contents into MongoDB database
    inserted = column.insert_many(files_json)
