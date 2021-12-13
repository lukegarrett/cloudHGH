
# Author: Camren Hall, Safet Hoxha, Luke Garrett
# CS4287-5287: Principles of Cloud Computing, Vanderbilt University
#
# Created: Sept 22, 2020
#
# Purpose:
#    Use Kafka consumer API to stream data to CouchDB

import json
import os   # need this for popen
import time # for sleep
from kafka import KafkaConsumer  # consumer of events

ip = "ec2-3-137-205-212.us-east-2.compute.amazonaws.com"
# acquire consumer

consumer = KafkaConsumer(bootstrap_servers="ec2-3-137-205-212.us-east-2.compute.amazonaws.com:9092", value_deserializer=lambda v: json.loads(v).decode('utf-8'))
# subscribe to topic
consumer.subscribe (topics=["tweetdata"])

# we keep reading and printing
for msg in enumerate(consumer):
    print (msg)

consumer.close ()
    






