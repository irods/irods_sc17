To Set the Demo machine iRODS and audit plugin was installed. RabbitMQ, Elastic Search and Logstash were also installed.

Ubuntu 16.04 LTS

Prepare and clone this workshop repository:
```
sudo apt-get -y install git python-pip
git clone https://github.com/trel/sc17
```

Install and configure iRODS 4.2.2:
```
wget -qO - https://packages.irods.org/irods-signing-key.asc | sudo apt-key add -
echo "deb [arch=amd64] https://packages.irods.org/apt/ $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/renci-irods.list
sudo apt-get update
sudo apt-get -y install irods-server irods-database-plugin-postgres postgresql
sudo -u postgres bash -c "psql -c \"create user irods with password 'testpassword';\""
sudo -u postgres bash -c "psql -c 'create database \"ICAT\";'"
sudo -u postgres bash -c "psql -c 'grant all privileges on database \"ICAT\" to irods;'"
sudo python /var/lib/irods/scripts/setup_irods.py < /var/lib/irods/packaging/localhost_setup_postgres.input
```

Install and configure iRODS Audit (AMQP) Rule Engine Plugin:
```
sudo apt-get -y install irods-rule-engine-plugin-audit-amqp
TODO ---- jq to jam the server_config.json with rule_engine and namespace...
```

Install RabbitMQ:
```
curl -s https://packagecloud.io/install/repositories/rabbitmq/rabbitmq-server/script.deb.sh | sudo bash
curl -s https://packagecloud.io/install/repositories/rabbitmq/erlang/script.deb.sh | sudo bash
sudo apt-get update
sudo apt-get -y install erlang
sudo apt-get -y install rabbitmq-server
sudo rabbitmq-plugins enable rabbitmq_amqp1_0
sudo service rabbitmq-server start
```

Verify Java8 is installed:
```
which java
java -version
```

Install and enable and start Elasticsearch:
```
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
sudo apt-get -y install apt-transport-https
echo "deb https://artifacts.elastic.co/packages/5.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-5.x.list
sudo apt-get update && sudo apt-get -y install elasticsearch
sudo systemctl enable elasticsearch.service
sudo service elasticsearch start
sudo service elasticsearch restart
curl http://localhost:9200
```

Install Logstash:
```
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
sudo apt-get update && sudo apt-get -y install logstash
sudo cp sc17/irods_audit.conf /etc/logstash/conf.d/irods_audit.conf
sudo service logstash start
```

Prepare to run `audit_storyteller.py`:
```
sudo -H pip install --upgrade pip
sudo -H pip install elasticsearch
```

Run `audit_storyteller.py`:
```
python audit_storyteller.py --data_object science.txt
```
