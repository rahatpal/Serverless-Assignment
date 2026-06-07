**Assignment 1: Automated EC2 Start/Stop Using Lambda**

**Architecture**

Lambda\
\|\
└── Boto3\
\|\
├── Find Action=Auto-Stop\
├── Stop Instances\
├── Find Action=Auto-Start\
└── Start Instances

**Step 1: Create EC2 Instances**

Create two EC2 instances:

**Instance 1**

Tag:

Key: Action\
Value: Auto-Stop

**Instance 2**

Tag:

Key: Action\
Value: Auto-Start

**Step 2: Create IAM Role**

IAM → Roles → Create Role

Trusted Entity:

AWS Service\
Lambda

Attach Policy:

AmazonEC2FullAccess

Role Name:

Lambda-EC2-Manager

**Step 3: Create Lambda Function**

Runtime:

Python 3.12

Execution Role:

Lambda-EC2-Manager

**Step 4: Lambda Code**

import boto3\
\
ec2 = boto3.client(\'ec2\')\
\
def lambda_handler(event, context):\
\
stop_instances = \[\]\
start_instances = \[\]\
\
response = ec2.describe_instances(\
Filters=\[\
{\
\'Name\': \'tag:Action\',\
\'Values\': \[\'Auto-Stop\'\]\
}\
\]\
)\
\
for reservation in response\[\'Reservations\'\]:\
for instance in reservation\[\'Instances\'\]:\
stop_instances.append(instance\[\'InstanceId\'\])\
\
if stop_instances:\
ec2.stop_instances(InstanceIds=stop_instances)\
\
response = ec2.describe_instances(\
Filters=\[\
{\
\'Name\': \'tag:Action\',\
\'Values\': \[\'Auto-Start\'\]\
}\
\]\
)\
\
for reservation in response\[\'Reservations\'\]:\
for instance in reservation\[\'Instances\'\]:\
start_instances.append(instance\[\'InstanceId\'\])\
\
if start_instances:\
ec2.start_instances(InstanceIds=start_instances)\
\
print(\"Stopped:\", stop_instances)\
print(\"Started:\", start_instances)\
\
return {\
\'statusCode\': 200\
}

**Expected Lambda Output**

Stopped: \[\'i-0ab123456789\'\]\
Started: \[\'i-0cd987654321\'\]

Screenshots

![](media/image1.png){width="6.5in" height="3.1993055555555556in"}

![](media/image2.png){width="6.5in" height="3.2041666666666666in"}

![](media/image3.png){width="6.5in" height="3.2041666666666666in"}

**Assignment 2: S3 Cleanup (Delete Files Older Than 30 Days)**

**Step 1: Create Bucket**

Example:

aws-cleanup-demo-bucket

Upload:

file1.txt\
file2.txt\
file3.txt

**Step 2: IAM Role**

Attach:

AmazonS3FullAccess

**Step 3: Lambda Code**

import boto3\
from datetime import datetime, timezone, timedelta\
\
s3 = boto3.client(\'s3\')\
\
BUCKET_NAME = \"aws-cleanup-demo-bucket\"\
\
def lambda_handler(event, context):\
\
cutoff = datetime.now(timezone.utc) - timedelta(days=30)\
\
response = s3.list_objects_v2(Bucket=BUCKET_NAME)\
\
for obj in response.get(\'Contents\', \[\]):\
\
if obj\[\'LastModified\'\] \< cutoff:\
\
s3.delete_object(\
Bucket=BUCKET_NAME,\
Key=obj\[\'Key\'\]\
)\
\
print(f\"Deleted: {obj\[\'Key\'\]}\")\
\
return {\
\'statusCode\': 200\
}

**Expected Output**

Deleted: old_backup.zip\
Deleted: old_logs.txt

**Screenshots**

![](media/image4.png){width="6.490277777777778in" height="3.192361111111111in"}

![](media/image5.png){width="6.490277777777778in" height="3.2020833333333334in"}

![](media/image6.png){width="6.490277777777778in" height="3.2118055555555554in"}

![](media/image7.png){width="6.5in" height="3.2020833333333334in"}

# Assignment 3: Detect Unencrypted S3 Buckets

## IAM Role

Attach:

AmazonS3ReadOnlyAccess

**Lambda Code**

import boto3

from botocore.exceptions import ClientError

s3 = boto3.client(\'s3\')

def lambda_handler(event, context):

encrypted_buckets = \[\]

unencrypted_buckets = \[\]

buckets = s3.list_buckets()

for bucket in buckets\[\'Buckets\'\]:

bucket_name = bucket\[\'Name\'\]

try:

s3.get_bucket_encryption(Bucket=bucket_name)

encrypted_buckets.append(bucket_name)

except ClientError as e:

error_code = e.response\[\'Error\'\]\[\'Code\'\]

if error_code == \'ServerSideEncryptionConfigurationNotFoundError\':

unencrypted_buckets.append(bucket_name)

print(\"=== Encryption Report ===\")

if unencrypted_buckets:

print(\"\nUnencrypted Buckets:\")

for bucket in unencrypted_buckets:

print(bucket)

else:

print(\"\nNo unencrypted buckets found.\")

print(\"\nEncrypted Buckets:\")

for bucket in encrypted_buckets:

print(f\"{bucket} - Encrypted\")

return {

\"statusCode\": 200,

\"message\": \"All buckets checked successfully\",

\"unencrypted_buckets\": unencrypted_buckets,

\"encrypted_buckets\": encrypted_buckets

}

Expected Output:

{

\"statusCode\": 200,

\"message\": \"All buckets checked successfully\",

\"unencrypted_buckets\": \[\],

\"encrypted_buckets\": \[

\"aws-cleanup-demo-rahat\",

\"test-bucket-01-rahat\",

\"test-bucket-02-rahat\"

\]

}

![](media/image8.png){width="6.490277777777778in" height="3.192361111111111in"}

![](media/image9.png){width="6.5in" height="3.2020833333333334in"}

![](media/image10.png){width="6.490277777777778in" height="3.2118055555555554in"}

![](media/image11.png){width="6.490277777777778in" height="3.095833333333333in"}

**Assignment 4: EBS Snapshot Automation**

**Step 1: Get Volume ID**

Example:

vol-0abcd123456789

**Step 2: IAM Role**

Attach:

AmazonEC2FullAccess

**Step 3: Lambda Code**

import boto3\
from datetime import datetime, timezone, timedelta\
\
ec2 = boto3.client(\'ec2\')\
\
VOLUME_ID = \"vol-0abcd123456789\"\
\
def lambda_handler(event, context):\
\
snapshot = ec2.create_snapshot(\
VolumeId=VOLUME_ID,\
Description=\"Automated Backup\"\
)\
\
print(\"Created Snapshot:\",\
snapshot\[\'SnapshotId\'\])\
\
cutoff = datetime.now(timezone.utc) - timedelta(days=30)\
\
snapshots = ec2.describe_snapshots(\
OwnerIds=\[\'self\'\]\
)\
\
for snap in snapshots\[\'Snapshots\'\]:\
\
if snap\[\'StartTime\'\] \< cutoff:\
\
ec2.delete_snapshot(\
SnapshotId=snap\[\'SnapshotId\'\]\
)\
\
print(\
\"Deleted:\",\
snap\[\'SnapshotId\'\]\
)\
\
return {\
\'statusCode\': 200\
}

**Expected Output**

Created Snapshot: snap-01ab234cd567\
\
Deleted: snap-09xy123zz456\
Deleted: snap-07gh987jk654

**Screenshot**

![](media/image12.png){width="6.490277777777778in" height="3.2118055555555554in"}

![](media/image13.png){width="6.5in" height="3.061111111111111in"}![](media/image14.png){width="6.490277777777778in" height="3.2118055555555554in"} ![](media/image15.png){width="6.5in" height="3.222916666666667in"}![](media/image16.png){width="6.480555555555555in" height="3.057638888888889in"}
