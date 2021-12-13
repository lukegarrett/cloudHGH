
# Author: Camren Hall, Safet Hoxha, Luke Garrett
# CS4287-5287: Principles of Cloud Computing, Vanderbilt University
#
# Created: Sept 22, 2020
#
# Purpose:
#    Use Kafka consumer API to stream data to CouchDB

import json
from kafka import KafkaConsumer  # consumer of events

# ip = "ec2-3-137-205-212.us-east-2.compute.amazonaws.com" #niu
# acquire consumer

consumer = KafkaConsumer(bootstrap_servers="129.114.24.229:9092", value_deserializer=lambda v: json.loads(v).decode('utf-8'))
# subscribe to topic
consumer.subscribe (topics=["tweetdata"])

# we keep reading and printing
for msg in enumerate(consumer):
    output = json.dumps(msg)
    myjson = json.loads(output)
    print(myjson[1])

consumer.close ()
    






