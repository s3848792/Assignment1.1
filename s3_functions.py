import boto3


# helper function to add list of image urls to Music Table response.
# replaces git image urls with s3 urls
# input: s3 bucket resource, Music Table response
# output: Altered Music Table
# 
# Phan, D. (2021) How to store and display media files using Python and Amazon S3 Buckets, Twilio Blog. Twilio. Available at: https://www.twilio.com/blog/media-file-storage-python-flask-amazon-s3-buckets (Accessed: April 7, 2023). 

def show_image(bucket, finalList):
    s3_client = boto3.client('s3')
    song_names = []
    x=0
    for i in finalList:
        song_names.append(i['title'])
    try:
        for item in s3_client.list_objects(Bucket=bucket)['Contents']:
            if song_names.count(item['Key'].removesuffix('.jpg'))>0:
                url = s3_client.generate_presigned_url('get_object', Params = {'Bucket': bucket, 'Key': item['Key']}, ExpiresIn = 100)
                finalList[x]['img_url']=url
    except Exception as e:
        pass


