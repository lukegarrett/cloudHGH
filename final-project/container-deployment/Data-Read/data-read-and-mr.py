import json
from operator import add
from kafka import KafkaProducer
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from decimal import Decimal
import couchdb


producer = KafkaProducer (bootstrap_servers="129.114.24.229:30000", value_serializer=lambda v: json.dumps(v).encode('ascii'))
producer.config

def func(x):
    if x[0][3] == 0:
        return ((x[0][0], x[0][1], x[0][2]), (x[1], 0))
    else:
        return ((x[0][0], x[0][1], x[0][2]), (0, x[1]))

if __name__ == "__main__":

    ip_couchdb = "129.114.27.39"
    user = "admin"
    password = "cloudhgh"
    spark = SparkSession\
        .builder\
        .appName("PythonEnergyAnalysis")\
        .getOrCreate()

    sc = spark.sparkContext


    # acquire couchdb server
    ip_couchdb = "129.114.27.39"
    user = "admin"
    password = "cloudhgh"
    conn_string  = "http://{}:{}@{}:30010".format(user, password, ip_couchdb)
    print(conn_string)
    couch = couchdb.Server(conn_string)
    dbname = "energy-data"

    if dbname in couch:
        db = couch[dbname]
    else:
        db = couch.create(dbname)
    
    emptyRDD = sc.emptyRDD()
    schema = StructType([
      StructField('value',DecimalType(),True), \
      StructField('property',IntegerType(),True), \
      StructField('plug_id',LongType(),True), \
      StructField('household_id',LongType(),True), \
      StructField('house_id',LongType(),True), \
    ])
    df = spark.createDataFrame(emptyRDD, schema)
    

    i = 0
    for docid in db.view('_all_docs'):
        data = [(Decimal(db[docid['id']]['value']), int(db[docid['id']]['property']),int(db[docid['id']]['plug_id']),int(db[docid['id']]['household_id']),int(db[docid['id']]['house_id']))]
        tmp = spark.createDataFrame(data, schema)
        df = df.union(tmp)
        print(i)
        i = i + 1
    finalRDD = df.rdd
    mappedRDD = finalRDD.map(lambda x: ((x[4],x[3],x[2],x[1]),x[0]))
    aTuple = (0,0)
    mappedRDD = mappedRDD.aggregateByKey(aTuple, lambda a,b: (a[0] + b, a[1] + 1), lambda a,b: (a[0] + b[0], a[1] + b[1]))
    mappedRDD = mappedRDD.mapValues(lambda v: v[0]/v[1])
    mappedRDD = mappedRDD.map(lambda x: func(x)).reduceByKey(lambda x,y: (x[0]+y[0], x[1]+y[1])).collect()
    
    if 'results' in couch:
        db2 = couch['results']
    else:
        db2 = couch.create('results')
    
    for (ident, vals) in mappedRDD:
            dict = {'house_id' : ident[0], 'household_id' : ident[1],'plug_id' : ident[2], 'average_work' : vals[0], 'average_load' : vals[1]}
            db2.save(dict)
    
    

    producer.close()
    spark.stop()

