# SC17 iRODS Workshop

## iRODS Consortium Update

## iRODS Technology Update

## Three Demonstrations

### Python Ingest Tool

### iRODS Audit (AMQP) Rule Engine Plugin

### iRODS Rule and Metadata-Driven Storage Tiering

Build and view the resource hierarchy:
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
ilsresc
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
