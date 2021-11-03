
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
import couchdb

ip_kafka = "172.17.0.6"
ip_couchdb = "172.17.0.7"
consumer = KafkaConsumer (bootstrap_servers="{}:9093".format(ip_kafka), value_deserializer=lambda v: json.loads(v).encode('ascii'))

consumer.subscribe (topics=["hghdata"])

# acquire couchdb server
user = "admin"
password = "password"
conn_string  = "http://{}:{}@{}:5984".format(user, password, ip_couchdb)
print(conn_string)
couch = couchdb.Server(conn_string)
dbname = "hghdata"

if dbname in couch:
    db = couch[dbname]
else:
    db = couch.create(dbname)

# we keep reading and printing
for msg in consumer:
    print (msg.value)
    document = json.loads(msg.value)
    #db.save(msg.value)
    #db.save({'type': 'Person', 'name': 'John Doe'})
    db.save(document)
consumer.close ()
    






