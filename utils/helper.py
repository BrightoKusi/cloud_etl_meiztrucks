import boto3


def create_bucket(access_key, secret_key, bucket_name, region):
    '''
    This creates an s3 bucket
    :args 
        access_key, secret_key, bucket_name, region 
    '''
    client = boto3.client(
        's3',
        aws_access_key_id= access_key,
        aws_secret_access_key= secret_key,
    )

    response = client.create_bucket(
    Bucket= bucket_name,
    CreateBucketConfiguration={
        'LocationConstraint': region,
    },
)


