#!/bin/bash
  
# turn on bash's job control
set -m
  
# Start the primary process and put it in the background
./kafka_2.13-2.8.1/bin/zookeeper-server-start.sh  ./kafka_2.13-2.8.1/config/zookeeper.properties &
./kafka_2.13-2.8.1/bin/kafka-server-start.sh  ./kafka_2.13-2.8.1/config/server.properties --override listeners=PLAINTEXT://:9092 &

# Start the helper process
sleep 10
./kafka_2.13-2.8.1/bin/kafka-topics.sh --create --topic hghdata --bootstrap-server localhost:9092
  
# the my_helper_process might need to know how to wait on the
# primary process to start before it does its work and returns
  
# now we bring the primary process back into the foreground
# and leave it there
fg %1