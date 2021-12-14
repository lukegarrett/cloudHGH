from operator import add
from pyspark.sql import *
from pyspark.sql.functions import *
import couchdb
    

# acquire couchdb server
ip_couchdb = "129.114.25.83"
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
  .option("kafka.bootstrap.servers", "129.114.25.83:30000") \
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