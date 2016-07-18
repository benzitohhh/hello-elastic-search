### Some examples using Python elastic search api:
#https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/index.html
# pip install elasticsearch

### Also consider checking Python elastic search DSL api (maybe easier for searching etc??):
### http://elasticsearch-dsl.readthedocs.io/en/latest/

from datetime import datetime
from elasticsearch import Elasticsearch


# To wipe the whole index:
### curl -XDELETE 'localhost:9200/my-index?pretty'


INDEX = "my-index"

ORGANISATION_DOC_TYPE = "organisation"

BOSE_CORP = {
    "assignees": [
        {
            "abbreviation": "BOSE CO LTD",
            "assignee_id": 703756,
            "size": 0,
            "sizeActive": 0
        },
        {
            "abbreviation": "BOSE CORP",
            "assignee_id": 3287,
            "size": 818,
            "sizeActive": 634,
            "human_readable_names": [
                {"name": "BOSE CORP",                                 "count": 139,    "similarity": 1.0       },
                {"name": "BOSE CORP.",                                "count": 15,     "similarity": 1.0       },
                {"name": "Bose Corporartion",                         "count": 1,      "similarity": 0.5       },
                {"name": "BOSE CORPORATION",                          "count": 721,    "similarity": 1.0       },
                {"name": "BOSE CORPORATION*EWC*",                     "count": 1,      "similarity": 0.5       },
                {"name": "Bose Corporation, a Delaware corporation",  "count": 12,     "similarity": 0.506159  },
                {"name": "BOSE CORPORATON",                           "count": 1,      "similarity": 0.5       },
                {"name": "Bose Corportion",                           "count": 1,      "similarity": 0.5       },
                {"name": "Bose Corproation",                          "count": 1,      "similarity": 0.5       },
                {"name": "HOOZU CORP",                                "count": 1,      "similarity": 0.00111982}
            ],
            "legal_entities": [
                {"legal_entity_id": 36306,     "source": "LEX_MACHINA",    "volume": 27},
                {"legal_entity_id": 76403,     "source": "KT_MINE",        "volume": 1 },
                {"legal_entity_id": 167121,    "source": "LEX_MACHINA",    "volume": 1 },
                {"legal_entity_id": 246530,    "source": "DISPUTE",        "volume": 0 }
            ]
        },
        {
            "abbreviation": "BOSE CORPORATIOIN",
            "assignee_id": 2014117,
            "size": 1,
            "sizeActive": 1
        },
        {
            "abbreviation": "BOSE CORPORATION THE MOUNTAIN",
            "assignee_id": 1916253,
            "size": 1,
            "sizeActive": 0
        },
        {
            "abbreviation": "BOSE INC",
            "assignee_id": 190931,
            "size": 0,
            "sizeActive": 0
        },
        {
            "abbreviation": "BOSE INC S",
            "assignee_id": 1574334,
            "size": 2,
            "sizeActive": 0,
            "human_readable_names": [
                {"name": "S. Bose, Inc.", "count": 1, "similarity": 1.0}
            ]
        },
        {
            "abbreviation": "BOSE LLC",
            "assignee_id": 703754,
            "size": 0,
            "sizeActive": 0,
            "legal_entities": [
                {"legal_entity_id": 154634,   "source": "PATENT_FREEDOM_OPCO",  "volume": 12}
            ]
        },
        {
            "abbreviation": "BOSE PROD INC",
            "assignee_id": 1829919,
            "size": 0,
            "sizeActive": 0,
            "human_readable_names": [
                {"name": "Bose Products, Inc.", "count": 1, "similarity": 1.0}
            ]
        },
        {
            "abbreviation": "THE BOSE CORPORATION",
            "assignee_id": 1917559,
            "size": 7,
            "sizeActive": 0
        }
    ],
    "eset": 3287,
    "name": "Bose Corporation",
    "size": 826,
    "sizeActive": 635
}

BOSE_INST = {
    "abbreviation": "",
    "assignees": [
        {
            "abbreviation": "BOSE INST",
            "assignee_id": 88762,
            "size": 18,
            "sizeActive": 11,
            "human_readable_names": [
                {"name": "BOSE INST",      "count": 1,   "similarity": 1.0},
                {"name": "BOSE INSTITUTE", "count": 4,   "similarity": 1.0}
            ]
        },
        {
            "abbreviation": "BOSE INST AND DEPT BIOTECHNOLOGY",
            "assignee_id": 703755,
            "size": 2,
            "sizeActive": 0
        },
        {
            "abbreviation": "BOSE NAT CENT BASIC SCI KOLKATA S N",
            "assignee_id": 1574333,
            "size": 1,
            "sizeActive": 1
        },
        {
            "abbreviation": "BOSE NAT CENT BASIC SCI S N",
            "assignee_id": 252857,
            "size": 11,
            "sizeActive": 6
        }
    ],
    "eset": 88762,
    "name": "Bose Institute",
    "size": 30,
    "sizeActive": 17
}


SANWA_BOSEI = {
    "abbreviation": "",
    "assignees": [
        {
            "abbreviation": "SANWA BOSEI KK",
            "assignee_id": 270675,
            "size": 7,
            "sizeActive": 0,
            "human_readable_names": [
                {"name": "SANWA BOUSEI, KK", "count": 6,  "similarity": 1.0}
            ]
        },
        {
            "abbreviation": "SANWA BUSEI KK",
            "assignee_id": 1007978,
            "size": 1,
            "sizeActive": 0,
            "human_readable_names": [
                {"name": "SANWA BOUSEI, KK", "count": 1, "similarity": 1.0}
            ]
        }
    ],
    "eset": 270675,
    "name": "SANWA BOSEI KK",
    "size": 8,
    "sizeActive": 0
}


# by default we connnect to localhost:9200
es = Elasticsearch()

# Add some documents
# es.index(index=INDEX, doc_type=ORGANISATION_DOC_TYPE, id=1, body=BOSE_SIMPLE)

# es.index(index=INDEX, doc_type=ORGANISATION_DOC_TYPE, id=2, body=BOSE_CORP)
# es.index(index=INDEX, doc_type=ORGANISATION_DOC_TYPE, id=3, body=BOSE_INST)
# es.index(index=INDEX, doc_type=ORGANISATION_DOC_TYPE, id=4, body=SANWA_BOSEI)

# And retrieve them
#es.get(index="my-index", doc_type="organisation", id=43)
