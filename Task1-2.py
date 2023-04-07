import boto3

def create_music_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')
    table = dynamodb.create_table(
        TableName='Music',
        KeySchema=[
            {
                'AttributeName': 'artist',
                'KeyType': 'HASH' # Partition key
            },
            {
                'AttributeName': 'title',
                'KeyType': 'RANGE' # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'artist',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'title',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
        )
    return table


if __name__ == '__main__':
    movie_table = create_music_table()
    print("Table status:", movie_table.table_status)