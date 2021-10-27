Luke Garrett
Camren Hall
Safet Hoxha

https://kubernetes.io/blog/2019/03/15/kubernetes-setup-using-ansible-and-vagrant/

Teamwork:
Because this was our first project we performed the majority of the tasks together in order to familiarize ourselves with working in the cloud.

Effort:
This project was definitely alot more difficult to complete than we had originally anticipated. The majority of our time was spent
setting up the instances of chameleon and AWS. Familiarizing ourselves with the couchdb api and formatting the data also took longer
than we had expected.

Workflow and notes from our experience:

Setting up AWS : First we created the 2 instances and paired them with 2 keys. After creating the instances, we created a security group to include allowing inbound connections 
on all the ports we needed, in order to set up our connections. Next we added the security groups to our instances. After that we noted the Public IPv4 DNS addresses for each.
Next we connected to our instances through the terminal, by using the key and the public IPv4 DNS address.
After that, we downloaded all the necessary java packets and updates in order to run kafka on our instances. We ran commands to download kafka, through url's in command line.
After downloading it, we unzipped and deleted the zip file. Next we modified the kafka server properties of both instances to fit our desired goal. 
On second instance, we started zookeeper. Then started the first server on the first instance, and started the second server on second instance.
On our second instance we created the topic.
Next we modified and worked on consumer and producer codes.
On producer we modified the values for topic name, its url connection, reading the data from a CSV file and sending it to the consumer.
On consumer we modified the values for topic name, its url connection, reading the data being sent from producer, printing it for debugging, and saved it on CouchDB.
Then the last step, was to run the producer which would send the data to the topic and run the consumer which would be subscribed to that topic.