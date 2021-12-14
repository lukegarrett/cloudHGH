import json
from operator import add
from kafka import KafkaProducer
from pyspark.sql import *
from pyspark.sql.functions import *
from decimal import Decimal
import couchdb
import time
    

# acquire couchdb server
ip_couchdb = "129.114.27.39"
user = "admin"
password = "cloudhgh"
conn_string  = "http://{}:{}@{}:30010".format(user, password, ip_couchdb)
couch = couchdb.Server(conn_string)
dbname = "updated-info"


spark = SparkSession \
    .builder \
    .appName("TwitterStockCount") \
    .getOrCreate()
spark.sparkContext.setLogLevel('WARN')

df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "129.114.27.196:9092") \
  .option("subscribe", "tweetdata") \
  .load()

df = df.selectExpr("timestamp", "CAST(value AS STRING)")
  
words = df.select(df.timestamp, explode(split(df.value, " ")).alias("word")).where("LEFT(word, 1) = '$' AND SUBSTRING(word,2,LENGTH(word)-1) REGEXP '^[A-Z]+$'")
windowedCounts = words.groupBy(
    window(words.timestamp, "5 minutes", "2 minutes"),
    words.word
).count().sort(['window','count'], ascending = False)





query2 = windowedCounts \
    .writeStream \
    .outputMode("complete") \
    .format("console") \
    .start()

query2.awaitTermination()

spark.stop()