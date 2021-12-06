
# Author: Camren Hall, Safet Hoxha, Luke Garrett
# CS4287-5287: Principles of Cloud Computing, Vanderbilt University
#
# Created: Sept 22, 2020
#
# Purpose:
#    Use Kafka consumer API to stream data to CouchDB

import json
import couchdb

ip_couchdb = "129.114.27.39"

# acquire couchdb server
user = "admin"
password = "cloudhgh"
conn_string  = "http://{}:{}@{}:30010".format(user, password, ip_couchdb)
print(conn_string)
couch = couchdb.Server(conn_string)
dbname = "mr-documents"

if dbname in couch:
    db = couch[dbname]
else:
    db = couch.create(dbname)

document = open('alice_in_wonderland.txt','r')

doc_id, doc_rev = db.save({'name': 'Alice in Wonderland', 'text': document.read()})

document.close()

for docid in db.view('_all_docs'):
    print(db[docid['id']])
    






