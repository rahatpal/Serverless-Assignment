import boto3
from datetime import datetime, timezone, timedelta

s3 = boto3.client('s3')

BUCKET_NAME = "aws-cleanup-demo-rahat"

def lambda_handler(event, context):

    cutoff = datetime.now(timezone.utc) - timedelta(days=30)

    response = s3.list_objects_v2(Bucket=BUCKET_NAME)

    for obj in response.get('Contents', []):

        if obj['LastModified'] < cutoff:

            s3.delete_object(
                Bucket=BUCKET_NAME,
                Key=obj['Key']
            )

            print(f"Deleted: {obj['Key']}")

    return {
        'statusCode': 200
    }
