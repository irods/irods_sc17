Deploying this code:  https://github.com/irods-contrib/irods_tools_ingest

Uses the PRC: https://github.com/irods/python-irodsclient

Two machines:
```
# iRODS 4.2.2 Server
rods/rods
172.25.14.119	icat.example.org icat
```
```
# Redis Server
172.25.14.120
sudo su - irodsbuild
source testenv3/bin/activate
```

Confirm the Redis service is running:
```
sudo service redis_6379 restart/status/start
```

Start the Redis Queue dashboard:
```
rq-dashboard 
```
View the dashboard at http://172.25.14.120:9181/

`irodsqueue ingest` is 2-3x faster than `iput -r`

