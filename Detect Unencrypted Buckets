import boto3
from botocore.exceptions import ClientError

s3 = boto3.client('s3')

def lambda_handler(event, context):

    encrypted_buckets = []
    unencrypted_buckets = []

    buckets = s3.list_buckets()

    for bucket in buckets['Buckets']:
        bucket_name = bucket['Name']

        try:
            s3.get_bucket_encryption(Bucket=bucket_name)
            encrypted_buckets.append(bucket_name)

        except ClientError as e:
            error_code = e.response['Error']['Code']

            if error_code == 'ServerSideEncryptionConfigurationNotFoundError':
                unencrypted_buckets.append(bucket_name)

    print("=== Encryption Report ===")

    if unencrypted_buckets:
        print("\nUnencrypted Buckets:")
        for bucket in unencrypted_buckets:
            print(bucket)
    else:
        print("\nNo unencrypted buckets found.")

    print("\nEncrypted Buckets:")
    for bucket in encrypted_buckets:
        print(f"{bucket} - Encrypted")

    return {
        "statusCode": 200,
        "message": "All buckets checked successfully",
        "unencrypted_buckets": unencrypted_buckets,
        "encrypted_buckets": encrypted_buckets
    }
