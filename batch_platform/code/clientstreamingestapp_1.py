from pandas import read_csv
from pandas import DataFrame
from random import randrange
import time
from datetime import datetime
from datetime import timedelta
import json
from mysimbdp import databroker, insert_coredms, subscribe_stream
# open database connection with MongoDB and PyMongo
#client = MongoClient(['localhost:27017', 'localhost:27018', 'localhost:27019'], replicaset='replicaset0')
def ingest(report_period=None):
    database_name = 'STREAMING_CUSTOMER_A'


    # establish Apache Kafka to subscribe events
    topic_name = '1084_top'

    consumer = subscribe_stream(topic_name)

    ts_date = datetime.today().strftime('%Y%m%d-%H%M%S')
    #log_file_name = "streaming-log-" + ts_date + ".log"
    #log_file = open(log_file_name, 'w')
    #log_file.write("status;part_id;ts_date;ts_time;room\n")

    # report objects for ingestion
    total_size = 0

    #initalize message counter
    messages_number = 0
    ingestion_times = []
    start_time = datetime.now()
    reported = 0
    for msg in consumer:
        tic = datetime.now()
        insert_coredms(database_name, msg.value)
        toc = datetime.now()
        message = msg.value
        #log_file.write("INSERTED" + ';'+ str(message['part_id']) + ';'+ str(message['ts_date']) + ';'+ str(message['ts_time']) + ';'+ str(message['room']) + '\n')
        total_size += len(msg.value)
        messages_number += 1
        ingestion_times.append((toc-tic))
        if (datetime.now() - start_time >= report_period) and reported == 0:
            report_file = open('ingestion-report-' + str(datetime.today().strftime('%Y%m%d-%H%M%S')) + ".log", 'w')
            #times = [ingestion_times[i-1] - ingestion_times[i] for i in range(1, len(ingestion_times))]
            #average_ingestion_time = sum(ingestion_times, timedelta(0)) / len(times)
            average_ingestion_time = report_period / messages_number
            report = {"messages": str(messages_number), "total_size": str(total_size), "average_ingestion_time": str(average_ingestion_time)}
            databroker(report, "REPORT")
            report_file.write(str(report))
            report_file.close()
            start_time = datetime.now()
            messages_number = 0


    #log_file.close()
