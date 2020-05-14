import clientstreamingestapp_1
import clientstreamingestapp_2
from datetime import timedelta
from mysimbdp import databroker
from kafka import KafkaConsumer
from multiprocessing import Process, Manager
import json
import os

# global list for processes
processes = []

# time period for reporting
time_period = timedelta(minutes=1)

def streamingestmanager(customer_ID=None):
    print("STREAMING MANAGER v0.1\n")
    print("Welcome to Streaming Manager!\n")
    print("---------------\n")
    print("Start to collect some data from IoT sensors\n")

    #customer_ID = input("Customer ID: ")
    #customer_ID = 'A'
    command = 'K'
    #command = input("To start data collection, please press K")
    print("To stop data collection, use Ctrl + C \n")
    print("Have a nice streaming!")

    if command == "K":
        if customer_ID == "A":
            clientstreamingestapp_1.ingest(time_period)
        if customer_ID == "B":
            clientstreamingestapp_2.ingest(time_period)

def receive_report():
    consumer = KafkaConsumer("REPORT", value_deserializer=lambda m: json.loads(m.decode('ascii')))
    for msg in consumer:
        if int(msg.value['messages']) < 10:
            print("Not enough messages during this time interval. Starting a new instance.")
            invoke_ingestion('A')
            invoke_ingestion('B')
        elif int(msg.value['messages']) >= 25:
            print("Enough messages, closing one instance to save resources.")
            #invoke_ingestion()
            #process.terminate()
        print(msg)

def invoke_ingestion(customer_ID):
    if customer_ID == 'A':
        new_instance = Process(target=clientstreamingestapp_1.ingest, args=(time_period,))
    if customer_ID == 'B':
        new_instance = Process(target=clientstreamingestapp_2.ingest, args=(time_period,))
    new_instance.start()
    processes.append(new_instance)
    new_instance.join()


if __name__ == '__main__':

    manager_process_A = Process(target=streamingestmanager, args=('A',))
    manager_process_B = Process(target=streamingestmanager, args=('B',))
    manager_process_A.start()
    manager_process_B.start()
    report_process = Process(target=receive_report)
    report_process.start()
    processes.append(manager_process_A)
    processes.append(manager_process_B)
    processes.append(report_process)
    manager_process_A.join()
    manager_process_B.join()
    report_process.join()
