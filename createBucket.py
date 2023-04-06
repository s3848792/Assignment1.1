import logging 
import boto3 
from botocore.exceptions import ClientError 

def create_bucket(bucket_name, region=None):


    s3 = boto3.client('s3') 
    response = s3.list_buckets() 
    print('Existing buckets before:') 
    for bucket in response['Buckets']: 
        print(f'  {bucket["Name"]}') 

    
    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)

    response = s3.list_buckets() 
    print('Existing buckets now:') 
    for bucket in response['Buckets']: 
        print(f'  {bucket["Name"]}') 


if __name__ == '__main__':
    create_bucket('s3848792assignment1test', 'ap-southeast-2')


