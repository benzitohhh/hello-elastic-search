# Elastic Search


# General stuff

```
Start server:     ./bin/elasticsearch
Health check:     curl 'localhost:9200/_cat/health?v'
list nodes:       curl 'localhost:9200/_cat/nodes?v'
list indices:     curl 'localhost:9200/_cat/indices?v'
```

General commands follow this form:
```
curl -X<REST Verb> <Node>:<Port>/<Index>/<Type>/<ID>
```

To create an index called "customer":
```
curl -XPUT 'localhost:9200/customer?pretty'
```

To add/replace a document to "customer" index (type is "external", id is "1"):
```
curl -XPUT 'localhost:9200/customer/external/1?pretty' -d '
{
  "name": "John Doe"
}'
```

To add a document (no id specified, so use POST - this will create a random hash id):
```
curl -XPOST 'localhost:9200/customer/external?pretty' -d '
{
  "name": "Jane Doe"
}'
```

To update (merges in fields rather than overwriting):
```
curl -XPOST 'localhost:9200/customer/external/1/_update?pretty' -d '
{
  "doc": { "name": "Jane Doe", "age": 20 }
}'
```

To retrieve document id=1 from the "customer" index (type is external)XS:
```
curl -XGET 'localhost:9200/customer/external/1?pretty'
```

To show all documents:
```
curl -XGET 'localhost:9200/customer/external/_search?pretty'
```

To search:
```
curl -XGET 'localhost:9200/customer/external/_search?pretty&q=someString'
```

To delete a document:
```
curl -XDELETE 'localhost:9200/customer/external/2?pretty'
```

To delete index customer
```
curl -XDELETE 'localhost:9200/customer?pretty'
```

Bulk with 2 replacements:

```
curl -XPOST 'localhost:9200/customer/external/_bulk?pretty' -d '
{"index":{"_id":"1"}}
{"name": "John Doe" }
{"index":{"_id":"2"}}
{"name": "Jane Doe" }
'
```

Bulk with one update, and one deletion:

```
curl -XPOST 'localhost:9200/customer/external/_bulk?pretty' -d '
{"update":{"_id":"1"}}
{"doc": { "name": "John Doe becomes Jane Doe" } }
{"delete":{"_id":"2"}}
'
```

To load in a dataset from bulk-format file accounts.json:
```
curl -XPOST 'localhost:9200/bank/account/_bulk?pretty' --data-binary "@accounts.json"
```

To search it (if no size specified, defaults to 10):
```
curl -XPOST 'localhost:9200/bank/_search?pretty' -d '
{
  "query": { "match_all": {} },
  "size": 1
}'
```

Search with a sort:
```
curl -XPOST 'localhost:9200/bank/_search?pretty' -d '
{
  "query": { "match_all": {} },
  "sort": { "balance": { "order": "desc" } }
}'
```

Search, and specify subset of fields to return:
```
curl -XPOST 'localhost:9200/bank/_search?pretty' -d '
{
  "query": { "match_all": {} },
  "_source": ["account_number", "balance"]
}'
```

Match (any of the words "mill" or "lane":
```
curl -XPOST 'localhost:9200/bank/_search?pretty' -d '
{
  "query": { "match": { "address": "mill lane" } }
}'
```

Match-phrase (match exact phrase "mill lane"):
```
curl -XPOST 'localhost:9200/bank/_search?pretty' -d '
{
  "query": { "match_phrase": { "address": "mill lane" } }
}'
```

Boolean match:
```
curl -XPOST 'localhost:9200/bank/_search?pretty' -d '
{
  "query": {
    "bool": {
      "should": [
        { "match": { "address": "mill" } },
        { "match": { "address": "lane" } }
      ]
    }
  }
}'
```

Boolean match:
```
curl -XPOST 'localhost:9200/bank/_search?pretty' -d '
{
  "query": {
    "bool": {
      "must": [
        { "match": { "age": "40" } }
      ],
      "must_not": [
        { "match": { "state": "ID" } }
      ]
    }
  }
}'
```

Boolean: query (match all) and filter
```
curl -XPOST 'localhost:9200/bank/_search?pretty' -d '
{
  "query": {
    "bool": {
      "must": { "match_all": {} },
      "filter": {
        "range": {
          "balance": {
            "gte": 20000,
            "lte": 30000
          }
        }
      }
    }
  }
}'
```

Aggregate - group by field:
```
curl -XPOST 'localhost:9200/bank/_search?pretty' -d '
{
  "size": 0,
  "aggs": {
    "group_by_state": {
      "terms": {
        "field": "state"
      }
    }
  }
}'
```

Nested aggregate - group by field, and get average:
```
curl -XPOST 'localhost:9200/bank/_search?pretty' -d '
{
  "size": 0,
  "aggs": {
    "group_by_state": {
      "terms": {
        "field": "state"
      },
      "aggs": {
        "average_balance": {
          "avg": {
            "field": "balance"
          }
        }
      }
    }
  }
}'
```


Nested Aggregate - group by field, get average, then sort by average desc
```
curl -XPOST 'localhost:9200/bank/_search?pretty' -d '
{
  "size": 0,
  "aggs": {
    "group_by_state": {
      "terms": {
        "field": "state",
        "order": {
          "average_balance": "desc"
        }
      },
      "aggs": {
        "average_balance": {
          "avg": {
            "field": "balance"
          }
        }
      }
    }
  }
}'
```

Nested Aggregate - group by age brackets, then by gender, then get avg account balance
```
curl -XPOST 'localhost:9200/bank/_search?pretty' -d '
{
  "size": 0,
  "aggs": {
    "group_by_age": {
      "range": {
        "field": "age",
        "ranges": [
          {
            "from": 20,
            "to": 30
          },
          {
            "from": 30,
            "to": 40
          },
          {
            "from": 40,
            "to": 50
          }
        ]
      },
      "aggs": {
        "group_by_gender": {
          "terms": {
            "field": "gender"
          },
          "aggs": {
            "average_balance": {
              "avg": {
                "field": "balance"
              }
            }
          }
        }
      }
    }
  }
}'
```


## Python

```
pip install elasticsearch
```
