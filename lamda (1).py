import json
import urllib.parse
import boto3
import requests
import csv
from io import StringIO

print('Loading function')

s3 = boto3.client('s3')


def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        
        body = response['Body'].read().decode('unicode_escape')
        file=StringIO(body)
        csv_read = csv.reader(file, delimiter=',')
        
        for line in csv_read:print(line)
        
        
        url_endpoint='https://esportz-regs.herokuapp.com/'
        
        r = requests.post(url_endpoint, files={'files': (key, response['Body'].read(), str(response['ContentType'])+';charset=utf8')})
        
        return {
            'code':1,
            'response':r.json()
        }
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
