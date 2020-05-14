from random import randrange
import time
from datetime import datetime
from mysimbdp import databroker
import json

'''
Simulated IoT sensor generating failing data.
'''

# SIMULATED IoT SENSOR for certain user
def testSensor_1(TEST_RATE, MAX_ITER=1000):
    '''
    Test sensor with very high sampling rate
    '''
    rooms = ['living room', 'kitchen', 'hall', 'bathroom']
    part_id = 1086
    run = 1
    topic_name = '1086'
    count = 0
    while 1:
        if count == MAX_ITER:
            return
        ts_date = datetime.today().strftime('%Y%m%d')
        ts_time = datetime.today().strftime('%H:%M:%S')
        room = randrange(4)
        message = {"part_id": part_id, "ts_date": ts_date, "ts_time": ts_time, "room": rooms[room]}

        #message = json.dumps(message)
        print(message)
        databroker(message, topic_name)
        time.sleep(TEST_RATE)
        count += 1

def testSensor_2(TEST_RATE, MAX_ITER=1000):
    '''
    Test sensor with wrong message format
    '''
    part_id = 1086
    run = 1
    topic_name = '1086'
    count = 0
    while 1:
        if count == MAX_ITER:
            return
        ts_date = datetime.today().strftime('%Y%m%d')
        ts_time = datetime.today().strftime('%H:%M:%S')
        message = "part_id: 1086 ts_date: 20191110 ts_time: 20:55:00 room: kitchen"

        #message = json.dumps(message)
        print(message)
        databroker(message, topic_name)
        time.sleep(TEST_RATE)
        count += 1
