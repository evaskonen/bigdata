from random import randrange
import time
from datetime import datetime
from mysimbdp import databroker
import json

'''
Simulated IoT sensor generating data about a person's indoor movements.
'''

# SIMULATED IoT SENSOR for certain user
rooms = ['living room', 'kitchen', 'hall', 'bathroom']
part_id = 1086
run = 1
topic_name = '1086'
while 1:
    ts_date = datetime.today().strftime('%Y%m%d')
    ts_time = datetime.today().strftime('%H:%M:%S')
    room = randrange(4)
    message = {"part_id": part_id, "ts_date": ts_date, "ts_time": ts_time, "room": rooms[room]}

    #message = json.dumps(message)
    print(message)
    databroker(message, topic_name)
    time.sleep(15)
