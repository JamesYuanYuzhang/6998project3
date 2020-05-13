import json
import boto3
from elasticsearch import Elasticsearch, helpers, RequestsHttpConnection
import certifi
from requests_aws4auth import AWS4Auth

def search_es(es,key1,key2):
    print(key1)
    print(key2)
    keys=[key for key in [key1,key2] if key is not None]
    res=[]
    for key in keys:
        query={"query":{"bool": {
                "should": [
                  { "term": { "labels": key }},
                ]
                        }
                }}
        response = es.search(index="photo", doc_type="_doc", body=query)
        print(response["hits"]["hits"])
        for hit in response["hits"]["hits"]:
            bucket,object_key=hit["_source"]["bucket"],hit["_source"]["objectKey"]
            url="https://s3.amazonaws.com/"+bucket+"/"+object_key
            res.append(url)
    return res


def lambda_handler(event, context):
    # TODO implement
    q=event["q"]
    client = boto3.client('lex-runtime')
    lex_response = client.post_text(
        botAlias='search',
        # 'Prod'
        botName='SearchPhoto',
        inputText=q,
        userId='search-photos',
    )
    key_1 = lex_response['slots']['key_first']
    key_2 = lex_response['slots']['key_second']
    host = "vpc-photos-x52tqixuetx5rwdao3a22se4tm.us-east-1.es.amazonaws.com"
    region = "us-east-1"
    service = "es"
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)
    es = Elasticsearch(hosts=[{"host": host, "port": 443, "use_ssl": True}], http_auth=awsauth, use_ssl=True,
                       verify_certs=True, connection_class=RequestsHttpConnection, request_timeout=30)
    res=search_es(es,key_1,key_2)
    return res

