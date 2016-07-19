# Nested example


# To show all documents:
curl -XGET 'localhost:9200/test-index/_search?pretty'


## To clear index:
curl -XDELETE 'localhost:9200/test-index?pretty'


## Add mapping (two-level nesting):
```
curl -PUT 'localhost:9200/test-index' -d '
{
  "mappings": {
    "organisation": {
      "properties": {
        "assignees": {
          "type": "nested",
          "properties": {
            "human_readable_names": {
              "type": "nested",
              "properties": {
                  "name": {
                      "type": "string"
                  },
                  "count": {
                      "type": "integer"
                  },
                  "similarity": {
                      "type": "float"
                  }
              }
            },
            "legal_entities": {
              "type": "nested",
              "properties": {
                  "volume": {
                      "type": "integer"
                  }
              }
            }
          }
        }
      }
    }
  }
}'
```


## Add 1 document
```
curl -PUT 'localhost:9200/test-index/organisation/1' -d '
{
    "name": "International Business Machines",
    "assignees": [
        {
            "abbreviation": "IBM",
            "human_readable_names": [
                { "name": "Big Blue", "count": 20, "similarity": 0.7 }
            ],
            "legal_entities": [
                { "name": "Computing-Tabulating-Recording Company",    "source": "LEX_MACHINA",    "volume": 27},
                { "name": "CTR",                                       "source": "KT_MINE",        "volume": 1 }
            ]
        }
    ]
}'
```


## Query by Org.name
Matches:     "INTERNATIONAL", "business", "Machines""
No matches:  "Int", "Machine", "ibm"
```
curl -XGET 'localhost:9200/test-index/_search?pretty' -d '
{
  "query": {
    "match": {
      "name": "International"
    }
  }
}'
```


## Query by Assignee.abbreviation:
Matches:     "ibm"
No matches:  "international"
```
curl -XGET 'localhost:9200/test-index/_search?pretty' -d '
{
  "query": {
    "nested": {
      "path": "assignees",
      "query": {
          "match": {
              "assignees.abbreviation": "IBM"
          }
      }
    }
  }
}'
```


## Query by Assignee.HumanReadableName.name (one-level nested query):
This does NOT work, as HumanReadableName is nested at second-level (hence out of scope).
```
curl -XGET 'localhost:9200/test-index/_search?pretty' -d '
{
  "query": {
    "nested": {
      "path": "assignees",
      "query": {
          "match": {
              "assignees.human_readable_names.name": "Big Blue"
          }
      }
    }
  }
}'
```


## Query by Assignee.HumanReadableName.name (two-level nested query):
Matches:     "big", "blue", "BIG BLUE"
No matches:  "international", "ibm"
```
curl -XGET 'localhost:9200/test-index/_search?pretty' -d '
{
  "query": {
    "nested": {
      "path": "assignees",
      "query": {
          "nested": {
              "path": "assignees.human_readable_names",
              "query": {
                  "match": {
                      "assignees.human_readable_names.name": "Big"
                  }
              }
          }
      }
    }
  }
}'
```


## Filter by Assignee.LegalEntity.volume (two-level nested query):
Matches:     gte 1, gte 27
No matches:  gte 28
```
curl -XGET 'localhost:9200/test-index/_search?pretty' -d '
{
  "query": {
    "nested": {
      "path": "assignees",
      "query": {
          "nested": {
              "path": "assignees.legal_entities",
              "query": {
                  "match_all": {},
                  "filter": {
                      "range": {
                          "assignees.legal_entities.volume": {
                              "gte": 1
                          }
                      }
                  }
              }
          }
      }
    }
  }
}'
```


## Query by Assignee.LegalEntity.name (two-level nested query):
Matches:     "ctr", "tabulating"
No matches:  "international", "ibm"
```
curl -XGET 'localhost:9200/test-index/_search?pretty' -d '
{
  "query": {
    "nested": {
      "path": "assignees",
      "query": {
          "nested": {
              "path": "assignees.legal_entities",
              "query": {
                  "match": {
                      "assignees.legal_entities.name": "ctr"
                  }
              }
          }
      }
    }
  }
}'
```
