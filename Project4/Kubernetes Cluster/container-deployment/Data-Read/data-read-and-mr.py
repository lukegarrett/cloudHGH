import json
from operator import add
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from decimal import Decimal
import couchdb
import time

curr = time.perf_counter()

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
    dbname = "hghdata"

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
    

    rowsTotal = db.view('_all_docs', include_docs=True)
    data = [(Decimal(rows['doc']['value']), int(rows['doc']['property']),int(rows['doc']['plug_id']),int(rows['doc']['household_id']),int(rows['doc']['house_id'])) for rows in rowsTotal]
    df = spark.createDataFrame(data, schema)
    curr2 = time.perf_counter()
    print('Downloading Complete. Time elapsed: ', (curr2 - curr))
    finalRDD = df.rdd
    mappedRDD = finalRDD.map(lambda x: ((x[4],x[3],x[2],x[1]),x[0]))
    aTuple = (0,0)
    mappedRDD = mappedRDD.aggregateByKey(aTuple, lambda a,b: (a[0] + b, a[1] + 1), lambda a,b: (a[0] + b[0], a[1] + b[1]))
    mappedRDD = mappedRDD.mapValues(lambda v: v[0]/v[1])
    mappedRDD = mappedRDD.map(lambda x: func(x)).reduceByKey(lambda x,y: (x[0]+y[0], x[1]+y[1])).collect()
    curr = time.perf_counter()
    print('Calculations Complete. Time elapsed: ', (curr - curr2))
    if 'results' in couch:
        db2 = couch['results']
    else:
        db2 = couch.create('results')
    
    f = open('results.txt', 'w')
    f.write('house_id\t\thousehold_id\t\tplug_id\t\taverage_work\t\taverage_load\n')
    for (ident, vals) in mappedRDD:
    	f.write(str(ident[0])+'\t\t'+str(ident[1])+'\t\t'+str(ident[2])+'\t\t'+str(vals[0])+'\t\t'+str(vals[1])+'\n')
            
    curr2 = time.perf_counter()
    print('Uploading Complete. Time elapsed: ', (curr2 - curr))
    
    spark.stop()
