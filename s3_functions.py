import boto3

def show_image(bucket, finalList):
    s3_client = boto3.client('s3')
    public_urls = []
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

# https://www.twilio.com/blog/media-file-storage-python-flask-amazon-s3-buckets