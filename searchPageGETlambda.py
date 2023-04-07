import json
import boto3
from boto3.dynamodb.conditions import Attr, Key
dynamodb = boto3.resource('dynamodb')

# handler method to retrieve searchj page music.
# scans for songs matching query values, and removes songs already subscribed to
# returns HTTP response, list in the body

def lambda_handler(event, context):
    
    music = dynamodb.Table('Music')
    subscriptions = dynamodb.Table('Subscriptions')
    musResponse = music.scan(FilterExpression=Attr('title').contains(event['title']) & Attr('artist').contains(event['artist']) & Attr('year').contains(event['year']))
    subResponse = subscriptions.query(KeyConditionExpression=Key('User').eq(event['username']))
    subSongs=[]
    if len(subResponse) > 0:
        for item in subResponse['Items']:
            subSongs.append(item['Song'])
        finalList = [x for x in musResponse['Items'] if not (subSongs.count(x['title'])>0)]


    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Credentials': 'true',
            'Content-Type': 'application/json'
        },
        'body': finalList
    }