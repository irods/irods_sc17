from __future__ import print_function

import json
import optparse
import pprint
import sys
from elasticsearch import Elasticsearch

def run_elasticsearch(data_object):
    es = Elasticsearch(hosts = [{"host":"localhost", "port":9200}])
    if es.indices.exists("irods_audit"):
          request_body = {
                          "sort" : [
                             {"@timestamp":{"order": "asc"}}
                          ],
                          "size" :10000,
                          "query": {
                             "bool": {
                               "must" : {
                                  "regexp": {"rule_name": "audit_pep_api_.*_pre"}
                               },
                               "must_not" : {
                                  "regexp": {"rule_name": "audit_pep_api_auth_.*_pre"}
                               }
                             }
                           }
                         }

           # sanity check
          res = es.search(index = "irods_audit", body=request_body)
          found = None
          for counter, hits in enumerate(res["hits"]["hits"]):
#              print(json.dumps(hits["_source"], sort_keys=True, indent=4, separators=(',',':')))
              for key, value in hits["_source"].iteritems():
                   if found is not None:
                       break
                   if data_object in value:
                       found = True

              if found is not None:
                  print(json.dumps(hits["_source"], sort_keys=True, indent=4, separators=(',',':')))
                  found = None

def main():
    parser = optparse.OptionParser()
    parser.add_option('-d', action='store', type='string', dest='data_object', help='logical path of data object to audit')
    (options, args) = parser.parse_args()
    if options.data_object is None or len(args) != 0:
        parser.error('-d data_object is required')
        return 1
    run_elasticsearch(options.data_object)

if __name__ == '__main__':
    sys.exit(main())
