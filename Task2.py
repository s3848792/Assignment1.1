import logging
import boto3
from botocore.exceptions import ClientError
import requests
from pathlib import Path

# method to upload images to specific S3 bucket, based on URLs from Music Table
# input: Music Table
# output: none
# results in the images uploaded to database
# fails if user not permitted, or images already uploaded.

def printImages(table):
    response = table.scan()
    data = response['Items']
    save_location = Path("/home/ubuntu/Assignment1/images")
    for item in  data:
        img_data = requests.get(item['img_url']).content
        filename = item['title'] + '.jpg'
        with open(save_location / 'image.jpg', 'wb') as handler:
            handler.write(img_data)
        s3_client = boto3.client('s3')
        try:
            response = s3_client.upload_file(save_location / 'image.jpg', 's3848792assignment1', filename)
        except ClientError as e:
            logging.error(e)
            return False
        return True

    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])

if __name__ == '__main__':
    dynamodb=None
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Music')
    printImages(table);