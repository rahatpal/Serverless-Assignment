import boto3

ec2 = boto3.client('ec2')

def lambda_handler(event, context):

    stop_instances = []
    start_instances = []

    response = ec2.describe_instances(
        Filters=[
            {
                'Name': 'tag:Action',
                'Values': ['Auto-Stop']
            }
        ]
    )

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            stop_instances.append(instance['InstanceId'])

    if stop_instances:
        ec2.stop_instances(InstanceIds=stop_instances)

    response = ec2.describe_instances(
        Filters=[
            {
                'Name': 'tag:Action',
                'Values': ['Auto-Start']
            }
        ]
    )

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            start_instances.append(instance['InstanceId'])

    if start_instances:
        ec2.start_instances(InstanceIds=start_instances)

    print("Stopped:", stop_instances)
    print("Started:", start_instances)

    return {
        'statusCode': 200
    }
