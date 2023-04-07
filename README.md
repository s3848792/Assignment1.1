# s3848792 CloudComputing Assignment 1

## Task 1 and 2

Task 1.1 was completed through the AWS dashboard, and is used for the project
Tasks 1.2, 1.3, and 2 can be found in the appropriate files, and run locally in the home directory through the commands:

>python3 task1-2.py

>python3 task1-3.py

>python3 task2.py

## Task 3

The website is hosted on my personal AWS account. 
The DynamoDB database, S3 storage, and EC2 instance are all a part of my personal account. 
The website can be run locally through the home directory as
>python3 Assignment1.py



### Advanced

Only two of the databse operations utilize Lambda and API functionality. They are the search page query function (GET) which returns music based on the query, and the subscribe feature (Post), which writes a new subscription to table. 

The lambda functions for these operations can be found respectively at 

>searchPageGETlambda

and 

>searchPagePOSTlambda

The api gateway is a simple REST API built as instructed in the labs, further details of which can be discussed in the demonstration.

## Miscellaneous

The production website can be found through the Public IPV4 DNS:

http://ec2-3-26-13-233.ap-southeast-2.compute.amazonaws.com

or IP:

3.26.13.233

The EC2 instance is hosted in the ap-southeast-2 region


The git repository of the src code can be found
>https://github.com/s3848792/Assignment1.1.git


WSGI code built on information found at:

>jQN, F.S. (2020) Boto3 and flask demystified, Medium. Medium. Available at: https://jqn.medium.com/boto3-and-flask-demystified-ecf9ab5804f4 (Accessed: April 5, 2023). 


