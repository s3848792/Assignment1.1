import boto3
dynamodb = boto3.resource('dynamodb')

# Method to create new subscription in DDB table
# Creates based on current user, and song picked
# returns copy of the event.
def lambda_handler(event, context):
        
        subscriptions = dynamodb.Table('Subscriptions')
        subscriptions.put_item(Item={'User': event['data']['user'],'Song': event['data']['song']})
        
        return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Credentials': 'true',
            'Content-Type': 'application/json'
        },
        'body': event
    }