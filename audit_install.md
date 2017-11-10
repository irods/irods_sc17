To Set the Demo machine iRODS and audit plugin was installed. RabbitMQ, Elastic Search and Logstash were also installed.

To Install RabbitMQ on UB16 run the following commands on the terminal
1.)	curl -s https://packagecloud.io/install/repositories/rabbitmq/rabbitmq-server/script.deb.sh | sudo bash
2.)	curl -s https://packagecloud.io/install/repositories/rabbitmq/erlang/script.deb.sh | sudo bash
3.)	sudo apt-get update
4.)	sudo apt-get -y install erlang
5.)	sudo apt-get -y install rabbitmq-server
6.)	sudo rabbitmq-plugins enable rabbitmq_amqp1_0
7.)	sudo service rabbitmq-server start

Before installing Elasticsearch and Logstash verify Java8 is installed on the system

To install Elasticsearch run the following commands on the terminal
1)	wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
2)	sudo apt-get install apt-transport-https
3)	sudo apt-get update && sudo apt-get install elasticsearch
4)	Let’s enable the service using this command sudo systemctl enable elasticsearch.service
5)	You can start the service as sudo service elasticsearch start
6)      To stop the service type sudo service elasticsearch stop

To install Logstash run the following commands on the terminal
1.)	wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
2.)	echo "deb https://artifacts.elastic.co/packages/5.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-5.x.list
3.)	sudo apt-get update && sudo apt-get install logstash
4.)	configuring logstash
i)	Create irods_audit.conf under /logstash/conf.d 
5.)	Start the service as sudo service logstash start


To run storytelling.py you will need to install the python wrapper for elasticsearch. To install that run the following command on the terminal
1.)    sudo pip install elasticsearch


Run storytelling.py by typing python storytelling.py --data_object "science.txt" on the command prompt 
