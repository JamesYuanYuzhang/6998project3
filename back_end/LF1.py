import json
import boto3
import datetime,time
from elasticsearch import Elasticsearch, helpers, RequestsHttpConnection
import certifi
from requests_aws4auth import AWS4Auth
BUCKET_NAME="hw3.yy2979"
KEY_NAME="1.jpeg"

def insert_record_es(es,record):
    response=es.index(index="photo",id=record["objectKey"],body=record)
    print(response['result'])

def get_record_es(es):
    response=es.get(index="photo",id="1.jpeg")
    print(response['_source'])

def lambda_handler(event, context):
    # TODO implement
    t0=time.time()
    host = "vpc-photos-x52tqixuetx5rwdao3a22se4tm.us-east-1.es.amazonaws.com"
    region = "us-east-1"
    service = "es"
    credentials = boto3.Session().get_credentials()
    try:
        awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)
    except:
        print(time.time()-t0)
    # es = Elasticsearch(hosts="https://vpc-restaurants-ljthbucz4jrosxjnru64urdd4q.us-east-1.es.amazonaws.com",ca_certs=certifi.where())
    es = Elasticsearch(hosts=[{"host": host, "port": 443, "use_ssl": True}], http_auth=awsauth, use_ssl=True,
                       verify_certs=True, connection_class=RequestsHttpConnection, request_timeout=30)
    BUCKET_NAME,KEY_NAME=event["Records"][0]["s3"]["bucket"]["name"],event["Records"][0]["s3"]["object"]["key"]
    client=boto3.client("rekognition")
    response = client.detect_labels(
        Image={
            'S3Object': {
                'Bucket': BUCKET_NAME,
                'Name': KEY_NAME
            }
        },
        MaxLabels=123,
        MinConfidence=55
    )
    print(json.dumps(response,indent=2))
    if response.get("Labels"):
        labels=[]
        for label in response["Labels"]:
            labels.append(label["Name"])
        print(labels)
        res=dict()
        res["objectKey"]=KEY_NAME
        res["bucket"]=BUCKET_NAME
        res["createdTimestamp"]=datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        res["labels"]=labels
        # res["_index"] = "image"
        # res["_type"] = "_doc"
        # res["_id"] =BUCKET_NAME+KEY_NAME
        insert_record_es(es,res)
        get_record_es(es,res)

        print(res,sep="\n")

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

# if __name__=="__main__":
#     event={
#   "Records": [
#     {
#       "eventVersion": "2.0",
#       "eventSource": "aws:s3",
#       "awsRegion": "us-west-2",
#       "eventTime": "1970-01-01T00:00:00.000Z",
#       "eventName": "ObjectCreated:Put",
#       "userIdentity": {
#         "principalId": "AIDAJDPLRKLG7UEXAMPLE"
#       },
#       "requestParameters": {
#         "sourceIPAddress": "127.0.0.1"
#       },
#       "responseElements": {
#         "x-amz-request-id": "C3D13FE58DE4C810",
#         "x-amz-id-2": "FMyUVURIY8/IgAtTv8xRjskZQpcIZ9KG4V5Wp6S7S/JRWeUWerMUE5JgHvANOjpD"
#       },
#       "s3": {
#         "s3SchemaVersion": "1.0",
#         "configurationId": "testConfigRule",
#         "bucket": {
#           "name": "hw3.yy2979",
#           "ownerIdentity": {
#             "principalId": "A3NL1KOZZKExample"
#           },
#           "arn": "arn:aws:s3:::hw3.yy2979"
#         },
#         "object": {
#           "key": "1.jpeg",
#           "size": 1024,
#           "eTag": "d41d8cd98f00b204e9800998ecf8427e",
#           "versionId": "096fKKXTRTtl3on89fVO.nfljtsv6qko"
#         }
#       }
#     }
#   ]
# }
#     context="111"
#     lambda_handler(event,context)