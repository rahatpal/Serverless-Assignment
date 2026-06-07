import boto3
from datetime import datetime, timezone, timedelta

ec2 = boto3.client('ec2')

VOLUME_ID = "vol-0abcd123456789"

def lambda_handler(event, context):

    snapshot = ec2.create_snapshot(
        VolumeId=VOLUME_ID,
        Description="Automated Backup"
    )

    print("Created Snapshot:",
          snapshot['SnapshotId'])

    cutoff = datetime.now(timezone.utc) - timedelta(days=30)

    snapshots = ec2.describe_snapshots(
        OwnerIds=['self']
    )

    for snap in snapshots['Snapshots']:

        if snap['StartTime'] < cutoff:

            ec2.delete_snapshot(
                SnapshotId=snap['SnapshotId']
            )

            print(
                "Deleted:",
                snap['SnapshotId']
            )

    return {
        'statusCode': 200
    }
