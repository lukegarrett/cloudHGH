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

    sc = spark.sparkContext


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
        print(data)
        rdd = sc.parallelize([data])
        print(rdd.collect())
        counts = rdd.flatMap(lambda x: x.split(' ')) \
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

