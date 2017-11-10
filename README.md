# SC17 iRODS Workshop

## iRODS Consortium Update

## iRODS Technology Update

## Three Demonstrations

### Python Ingest Tool

rods/rods
172.25.14.119	icat.example.org icat



172.25.14.120
sudo su - irodsbuild
source testenv3/bin/activate

sudo service redis_6379 restart/status/start

rq-dashboard 

http://172.25.14.120:9181/

`irodsqueue ingest` is about 3x faster than `iput -r`

pip freeze > requirements.txt
arrow==0.10.0
click==6.7
Flask==0.12.2
irodsqueue==0.1.0a0
itsdangerous==0.24
Jinja2==2.10
MarkupSafe==1.0
prettytable==0.7.2
python-dateutil==2.6.1
python-irodsclient==0.7.0a0
redis==2.10.6
rq==0.9.1
rq-dashboard==0.3.10
six==1.11.0
Werkzeug==0.12.2
xmlrunner==1.7.7


### iRODS Rule and Metadata-Driven Storage Tiering

README:
  https://github.com/irods/irods_training/tree/master/advanced/storage_tiering

Build the resource hierarchy:
```
iadmin mkresc ufs0 unixfilesystem `hostname`:/tmp/irods/ufs0
iadmin mkresc ufs1 unixfilesystem `hostname`:/tmp/irods/ufs1
iadmin mkresc ufs2 unixfilesystem `hostname`:/tmp/irods/ufs2
iadmin mkresc ufs3 unixfilesystem `hostname`:/tmp/irods/ufs3
iadmin mkresc ufs4 unixfilesystem `hostname`:/tmp/irods/ufs4
iadmin mkresc ufs5 unixfilesystem `hostname`:/tmp/irods/ufs5
iadmin mkresc rnd0 random
iadmin mkresc rnd1 random
iadmin mkresc rnd2 random
iadmin addchildtoresc rnd0 ufs0
iadmin addchildtoresc rnd0 ufs1
iadmin addchildtoresc rnd1 ufs2
iadmin addchildtoresc rnd1 ufs3
iadmin addchildtoresc rnd2 ufs4
iadmin addchildtoresc rnd2 ufs5
```

View the new resource hierarchy:
```
$ ilsresc
rnd0:random
├── ufs0:unixfilesystem
└── ufs1:unixfilesystem
rnd1:random
├── ufs2:unixfilesystem
└── ufs3:unixfilesystem
rnd2:random
├── ufs4:unixfilesystem
└── ufs5:unixfilesystem
```

Configure the tier group `example_group` and migration times with metadata:
```
imeta add -R rnd0 irods::storage_tier_group example_group 0
imeta add -R rnd1 irods::storage_tier_group example_group 1
imeta add -R rnd2 irods::storage_tier_group example_group 2
imeta add -R rnd0 irods::storage_tier_time 30
imeta add -R rnd1 irods::storage_tier_time 60
```

Configure the middle tier query to detect policy violations:
```
imeta set -R rnd1 irods::storage_tier_query "select META_DATA_ATTR_VALUE, DATA_NAME, COLL_NAME where RESC_NAME = 'ufs2' || = 'ufs3' and META_DATA_ATTR_NAME = 'irods::access_time' and META_DATA_ATTR_VALUE < 'TIME_CHECK_STRING'"
```

Teardown:
```
iadmin rmchildfromresc rnd0 ufs0
iadmin rmchildfromresc rnd0 ufs1
iadmin rmchildfromresc rnd1 ufs2
iadmin rmchildfromresc rnd1 ufs3
iadmin rmchildfromresc rnd2 ufs4
iadmin rmchildfromresc rnd2 ufs5
iadmin rmresc rnd0
iadmin rmresc rnd1
iadmin rmresc rnd2
iadmin rmresc ufs0
iadmin rmresc ufs1
iadmin rmresc ufs2
iadmin rmresc ufs3
iadmin rmresc ufs4
iadmin rmresc ufs5
iadmin rum
```

### iRODS Audit (AMQP) Rule Engine Plugin

[Demo](audit_install.md)
