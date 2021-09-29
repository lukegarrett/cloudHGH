
# Author: Camren Hall, Safet Hoxha, Luke Garrett
# CS4287-5287: Principles of Cloud Computing, Vanderbilt University
#
# Created: Sept 22, 2020
#
# Purpose:
#    Use Kafka consumer API to stream data to CouchDB

import json
import os   # need this for popen
from kafka import KafkaConsumer  # consumer of events
# import couchdb

ip = "ec2-3-137-205-212.us-east-2.compute.amazonaws.com"
consumer = KafkaConsumer (bootstrap_servers="{}:9092".format(ip))
consumer.subscribe (topics=["hghdata"])

# acquire couchdb server
# user = "admin"
# password = "teamhgh"
# conn_string  = "https://{}:{}@{}:5984".format(user, password, ip)
# print(conn_string)
# couch = couchdb.Server(conn_string)
# db = couch.create('hghdata')

# we keep reading and printing
for msg in consumer:
    print (msg)
consumer.close ()
    





