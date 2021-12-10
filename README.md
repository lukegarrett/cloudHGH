# Project Title

Principles of Cloud Computing Distributed Data Processing Cluster

## Authors

Luke Garrett
Camren Hall
Safet Hoxha

## Description

Deployment Technology: Vagrant, Ansible, Docker, Kubernetes, Kafka, CouchDB

This ground-up implementation begins by initializing a virtual machine on the user's OS through Vagrant. After the local Vagrant VM has been initialized, Vagrant will run a series of Ansible playbooks. The Ansible playbooks are responsible for spinning up two computing instances on OpenStack Chameleon Cloud.

One of the Openstack virtual machines, herein referred to as VM1, is responsible for:
* Acting as the Master node in the Kubernetes cluster
* Acting as a Kafka broker inside a Kubernetes Pod
* Acting as the primary CouchDB server inside a Kubernetes Pod.

The other Openstack virtual machine, herein referred to as VM2, is responsible for:
* Acting as a Worker node in the Kubernetes cluster
* Acting as a secondary Kafka broker joined with the overall Kubernetes cluster

## Getting Started

### Dependencies

* Vagrant configured with VirtualBox on local machine
* All other dependencies are handled virtually by Ansible and Docker

### Installing

* VirtualBox must be installed on the user's machine
* Vagrant must be installed on the user's machine
* All other dependencies are handled virtually by Ansible and Docker

### Executing program

In the root directory of this cloned project, run
```
vagrant up
```
followed by

```
vagrant provision
```

To execute the producer code responsible for sending data to the Kafka broker, navigate to ./Project1/ and run 

```
python new_producer.py
```

(or python3 if version conflicts arise)

Afterwards, the producer.py will send data to the Kafka broker, which will be available on VM1's CouchDB panel.

By default, this address is http://129.114.27.39:30010/_utils/

