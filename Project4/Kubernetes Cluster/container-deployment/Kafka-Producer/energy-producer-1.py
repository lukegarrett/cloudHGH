#
#
# Author: Aniruddha Gokhale
# CS4287-5287: Principles of Cloud Computing, Vanderbilt University
#
# Created: Sept 6, 2020
#

import json
import os   # need this for popen
import time # for sleep
from kafka import KafkaProducer  # producer of events
import csv

producer = KafkaProducer (bootstrap_servers="129.114.24.229:30000", value_serializer=lambda v: json.dumps(v).encode('ascii'), batch_size=1000000)
producer.config

with open("energy-sorted1M-1.csv", mode='r') as infile:
    reader = csv.reader(infile)
    count = 0
    while (next(reader)):
        for x in range(1000):
            row = next(reader)
            dict = {'id' : row[0], 'timestamp' : row[1], 'value' : row[2], 'property' : row[3],
                    'plug_id' : row[4], 'household_id' : row[5], 'house_id' : row[6]}
            json_dict = json.dumps(dict)
            producer.send('hghdata', json_dict)
        count += 1000
        print("finished 1000")
        print(count)

producer.close ()
    


        