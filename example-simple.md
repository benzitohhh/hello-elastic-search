# Example simple


# To show all documents:
curl -XGET 'localhost:9200/example-simple/_search?pretty'


## To clear index:
curl -XDELETE 'localhost:9200/example-simple?pretty'


## Add mapping (two-level nesting):
```
curl -PUT 'localhost:9200/example-simple' -d '
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
curl -PUT 'localhost:9200/example-simple/organisation/1' -d '
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
Matches:     "INTERNATIONAL", "business", "Machines", "Int", "Machine"
No matches:  "ibm"
```
curl -XGET 'localhost:9200/example-simple/_search?pretty' -d '
{
  "query": {
    "match_phrase_prefix": {
      "name": "International"
    }
  }
}'
```


## Query by Assignee.abbreviation:
Matches:     "ibm"
No matches:  "international"
```
curl -XGET 'localhost:9200/example-simple/_search?pretty' -d '
{
  "query": {
    "nested": {
      "path": "assignees",
      "query": {
          "match_phrase_prefix": {
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
curl -XGET 'localhost:9200/example-simple/_search?pretty' -d '
{
  "query": {
    "nested": {
      "path": "assignees",
      "query": {
          "match_phrase_prefix": {
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
curl -XGET 'localhost:9200/example-simple/_search?pretty' -d '
{
  "query": {
    "nested": {
      "path": "assignees",
      "query": {
          "nested": {
              "path": "assignees.human_readable_names",
              "query": {
                  "match_phrase_prefix": {
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
curl -XGET 'localhost:9200/example-simple/_search?pretty' -d '
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
curl -XGET 'localhost:9200/example-simple/_search?pretty' -d '
{
  "query": {
    "nested": {
      "path": "assignees",
      "query": {
          "nested": {
              "path": "assignees.legal_entities",
              "query": {
                  "match_phrase_prefix": {
                      "assignees.legal_entities.name": "ctr"
                  }
              }
          }
      }
    }
  }
}'
```


## TODO:
## 1) hybrid query (all_fields)
## 2) hybrid query (boolean)
## 3) add filter - either is_grouped, or (!is_grouped & (size>0 || litigation_volume>0 ))


## Hybrid query (all_fields)
Checks at Org, Assignee and HRN levels.
```
curl -XGET 'localhost:9200/example-simple/_search?pretty' -d '
{
  "query": {
    "match_phrase_prefix": {
      "_all": "XXX"
    }
  }
}'
```


## Hybrid query (boolean)
Checks at Org, Assignee and HRN levels.
```
curl -XGET 'localhost:9200/example-simple/_search?pretty' -d '
{
    "query": {
        "bool": {
            "should": [
                {
                    "match_phrase_prefix": { "name": "XXX" }
                },

                {
                    "query": {
                        "nested": {
                            "path": "assignees",
                            "query": {
                                "match_phrase_prefix": {
                                    "assignees.abbreviation": "XXX"
                                }
                            }
                        }
                    }
                },

                {
                    "query": {
                        "nested": {
                            "path": "assignees",
                            "query": {
                                "nested": {
                                    "path": "assignees.human_readable_names",
                                    "query": {
                                        "match_phrase_prefix": {
                                            "assignees.human_readable_names.name": "XXX"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }

            ]
        }
    }
}'
```



