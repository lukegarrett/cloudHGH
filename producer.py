from csv import reader
import json
import time
from kafka import KafkaProducer

producer = KafkaProducer (bootstrap_servers="localhost:9092",
                                          acks=1)

with open('national-history.csv', 'r') as read_obj:
    csv_reader = reader(read_obj)
    header = next(csv_reader)
    if header != None:
        for row in csv_reader:
            dic = {'date' : row[0], 'death' : row[1], 'deathIncrease' : row[2], 'inIcuCumulative' : row[3],
                   'inIcuCurrently' : row[4], 'hospitalizedIncrease' : row[5], 'hospitalizedCurrently' : row[6],
                   'hospitalizedCurrently' : row[7], 'negative' : row[8], 'negativeIncrease' : row[9],
                   'onVentilatorCumulative' : row[10], 'onVentilatorCurrently' : row[11], 'positive' : row[12],
                   'positiveIncrease' : row[13], 'states' : row[14], 'totalTestResults' : row[15],
                   'totalTestResultsIncrease' : row[16]}
            json_string = json.dumps(dic)
            producer.send("hghdata", value=bytes (json_string, 'ascii'))
            producer.flush()

            time.sleep(1)

producer.close()
