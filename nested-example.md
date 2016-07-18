# Nested example


## To clear these indecies:

curl -XDELETE 'localhost:9200/index-1?pretty'

curl -XDELETE 'localhost:9200/index-2?pretty'



# To show all documents:

curl -XGET 'localhost:9200/index-1/_search?pretty'

curl -XGET 'localhost:9200/index-2/_search?pretty'



## By default... inner arrays get flattenned:

```
curl -PUT 'localhost:9200/index-1/my_type/1' -d '
{
  "group" : "fans",
  "user" : [
    {
      "first" : "John",
      "last" :  "Smith"
    },
    {
      "first" : "Alice",
      "last" :  "White"
    }
  ]
}'


curl -XGET 'localhost:9200/index-1/my_type/_search?pretty'


curl -XGET 'localhost:9200/index-1/my_type/_search?pretty' -d '
{
  "query": {
    "bool": {
      "must": [
        { "match": { "user.first": "Alice" }},
        { "match": { "user.last":  "Smith" }}
      ]
    }
  }
}'

```

## So... use nesting:

```
curl -PUT 'localhost:9200/index-2' -d '
{
  "mappings": {
    "my_type": {
      "properties": {
        "user": {
          "type": "nested"
        }
      }
    }
  }
}'

curl -PUT 'localhost:9200/index-2/my_type/1' -d '
{
  "group" : "fans",
  "user" : [
    {
      "first" : "John",
      "last" :  "Smith"
    },
    {
      "first" : "Alice",
      "last" :  "White"
    }
  ]
}'

curl -XGET 'localhost:9200/index-2/_search?pretty' -d '
{
  "query": {
    "nested": {
      "path": "user",
      "query": {
        "bool": {
          "must": [
            { "match": { "user.first": "Alice" }},
            { "match": { "user.last":  "Smith" }}
          ]
        }
      }
    }
  }
}'

curl -XGET 'localhost:9200/index-2/_search?pretty' -d '
{
  "query": {
    "nested": {
      "path": "user",
      "query": {
        "bool": {
          "must": [
            { "match": { "user.first": "Alice" }},
            { "match": { "user.last":  "White" }}
          ]
        }
      },
      "inner_hits": {
        "highlight": {
          "fields": {
            "user.first": {}
          }
        }
      }
    }
  }
}'


curl -XGET 'localhost:9200/index-2/_search?pretty' -d '
{
  "query": {
    "nested": {
      "path": "user",
      "query": {
        "bool": {
          "must": [
            { "match": { "user.first": "Alice" }},
            { "match": { "user.last":  "White" }}
          ]
        }
      },
      "inner_hits": {
        "highlight": {
          "fields": {
            "user.first": {}
          }
        }
      }
    }
  }
}'

```
