import json
import os
from os import listdir
from kafka import KafkaConsumer, KafkaProducer
from pandas import DataFrame
import pandas as pd
from datetime import datetime
from pymongo import MongoClient

def fetchdata(directory_path):
    '''
    This method implements the mysimbdp-fetchdata
    '''
    # input: directory path as a string
    # output: staged file contents in a pandas dataframe
    # read constraint configuration file
    with open('constraints.json') as file:
        constraints = json.load(file)

    max_size = constraints['file_size']
    max_files = constraints['number_of_files']
    #directory_path = '/client-input-directory'
    #directory_path = 'C:/Users/Eero/bigdataplatforms/assignment-2-478360/data'
    n = 0 # number of iterations
    files = []
    # go through files in client-input-directory
    # calculate size of files and the number of files
    # if either of constraints is fulfilled, the execution stops
    # also, create a log file
    ts_date = datetime.today().strftime('%Y%m%d-%H%M%S')
    log_file_name = "log-" + ts_date + ".log"
    log_file = open(log_file_name, 'w')

    for file in os.listdir(directory_path):
        if n == max_files:
            break
        fp = os.path.join(directory_path, file)
        if os.path.getsize(fp) <= max_size:
            files.append(fp)
            log_file.write('SUCCESS: ' + datetime.today().strftime('%Y-%m-%d-%H:%M:%S') + " " + fp + " " + str(os.path.getsize(fp)) + " bytes \n")
        else:
            log_file.write('FAILED: ' + datetime.today().strftime('%Y-%m-%d-%H:%M:%S') + " " + fp + " " + str(os.path.getsize(fp)) + " bytes \n")
            print("File " + str(fp) + " is too large (>" + str(max_size) + " bytes).")
        n += 1

    log_file.close()

    # INSERT FILE CONTENTS INTO PANDAS DATAFRAME
    df_list = []
    if len(files) > 0:
        for file in files:
            df = pd.read_csv(file)
            df_list.append(df)
        df_all = pd.concat(df_list, axis=0, ignore_index=True)
    else:
        df_all = None
    return df_all


def databroker(message, topic_name):
    '''
    This method implements the mysimbdp-databroker.
    Data should be in list where each message is in
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
