
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
import couchdb

ip = "ec2-3-137-205-212.us-east-2.compute.amazonaws.com"
# acquire consumer

consumer = KafkaConsumer(bootstrap_servers="ec2-3-137-205-212.us-east-2.compute.amazonaws.com:9092", value_deserializer=lambda v: json.loads(v).decode('utf-8'))
# subscribe to topic
consumer.subscribe (topics=["hghdata"])

# acquire couchdb server
user = "admin"
password = "teamhgh"
conn_string  = "http://{}:{}@{}:5984".format(user, password, ip)
print(conn_string)
couchserver = couchdb.Server(conn_string)

dbname = "hghdata"
if dbname in couchserver:
    db = couchserver[dbname]
else:
    db = couchserver.create(dbname)
    
data = {}

# we keep reading and printing
for i, msg in enumerate(consumer):
    print ("consumer entrypoint")
    print (msg)
    data[i] = msg
    if (i > 15):
        break
db.save(data)
print("Upload should be completed")
consumer.close ()
    






