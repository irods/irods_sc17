
Ubuntu 16.04 LTS

Amazon   ssh -i training.pem ubuntu@34.230.40.77

vSphere 172.25.14.81


Prepare and clone this workshop repository:
```
sudo apt-get update
sudo apt-get -y install git python-pip moreutils jq
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
sudo cat /etc/irods/server_config.json | jq '.plugin_configuration.rule_engines += [{"instance_name": "irods_rule_engine_plugin-audit_amqp-instance","plugin_name": "irods_rule_engine_plugin-audit_amqp","plugin_specific_configuration" : {"amqp_location" : "ANONYMOUS@localhost:5672","amqp_options" : "","amqp_topic" : "audit_messages","pep_regex_to_match" : "audit_.*"}}]' | sudo sponge /etc/irods/server_config.json
sudo cat /etc/irods/server_config.json | jq '.rule_engine_namespaces += ["audit_"]' | sudo sponge /etc/irods/server_config.json
sudo chown irods:irods /etc/irods/server_config.json
sudo service irods restart
```

Install RabbitMQ:
```
curl -s https://packagecloud.io/install/repositories/rabbitmq/rabbitmq-server/script.deb.sh | sudo bash
curl -s https://packagecloud.io/install/repositories/rabbitmq/erlang/script.deb.sh | sudo bash
sudo apt-get update
sudo apt-get -y install erlang
sudo apt-get -y install rabbitmq-server
sudo rabbitmq-plugins enable rabbitmq_amqp1_0
sudo rabbitmq-plugins enable rabbitmq_management
sudo cp sc17/audit/rabbitmq.conf /etc/rabbitmq/rabbitmq.conf
sudo service rabbitmq-server start
sudo rabbitmqctl add_user test test
sudo rabbitmqctl set_user_tags test administrator
sudo rabbitmqctl set_permissions -p / test ".*" ".*" ".*"

```

The RabbitMQ dashboard is now available at http://`IP`:15672 and test/test.

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
curl -XPUT 'http://localhost:9200/irods_audit'
curl -XPUT localhost:9200/irods_audit/_mapping/hostname_mapping -d '
{
  "properties": {
    "hostname": {
       "type": "string",
      "index": "not_analyzed"
    }
  }
}'
```

Install Logstash:
```
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
sudo apt-get update && sudo apt-get -y install logstash
sudo cp sc17/audit/irods_audit.conf /etc/logstash/conf.d/irods_audit.conf
sudo service logstash start
```

Prepare to run `storyteller.py`:
```
sudo -H pip install --upgrade pip
sudo -H pip install elasticsearch
```

Run `storyteller.py`:
```
python sc17/audit/storyteller.py -d science.txt
```

To view all the PEPs (rather than a subset) now stored in Elasticsearch:
```
curl -XGET 'localhost:9200/irods_audit/_search?pretty' -H 'Content-Type: application/json' -d'
{
    "sort" : [
        {"@timestamp":{"order": "asc"}}
    ],
    "size" :10000,
    "query": {
        "match_all": {}
    }
}
'
```
