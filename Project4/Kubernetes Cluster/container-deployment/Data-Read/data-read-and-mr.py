#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

### THIS RUNS INSIDE A KUBERNETES POD AND NEEDS TO BE COPIED INTO THE POD

import json
from operator import add
from kafka import KafkaProducer
from pyspark.sql import SparkSession
import couchdb



producer = KafkaProducer (bootstrap_servers="129.114.24.229:30000", value_serializer=lambda v: json.dumps(v).encode('ascii'))
producer.config


if __name__ == "__main__":

    spark = SparkSession\
        .builder\
        .appName("PythonWordCount")\
        .getOrCreate()
    
    sparkContext = spark.sparkContext

    
    # acquire couchdb server
    ip_couchdb = "129.114.27.39"
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

    for docid in db.view('_all_docs'):

        data = str(db[docid['id']]['text'])
        dataframe = 
        lines = spark.read.text('alice_in_wonderland.txt').rdd.map(lambda r: r[0])
        counts = lines.flatMap(lambda x: x.split(' ')) \
                    .map(lambda x: (x, 1)) \
                    .reduceByKey(add)
        output = counts.collect()
        for (word, count) in output:
            dict = {word : count}
            json_dict = json.dumps(dict)
            producer.send('hghdata', json_dict)
            print("%s: %i" % (word, count))

    producer.close()
    spark.stop()
    

