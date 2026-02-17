import boto3

# Create EC2 resource and client
ec2_resource = boto3.resource('ec2')
ec2_client = boto3.client('ec2')

# Launch the instance
instances = ec2_resource.create_instances(
    ImageId='ami-0938a60d87953e820',  # AMI to launch
    MinCount=1,
    MaxCount=1,
    InstanceType='t2.micro',
    KeyName='nodejskey',
    BlockDeviceMappings=[
        {
            'DeviceName': '/dev/sda1',
            'Ebs': {
                'VolumeSize': 20,
                'VolumeType': 'gp2',
                'DeleteOnTermination': False
            }
        }
    ],
    UserData='''#!/bin/bash
    sudo apt update -y
    sudo apt install apache2 -y
    sudo systemctl start apache2
    sudo systemctl enable apache2
    echo "<html><body><h1>Welcome to Apache Web Server - Srujal Shah</h1></body></html>" | sudo tee /var/www/html/index.html
    sudo ufw allow 'Apache'
    ''',
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {'Key': 'Name', 'Value': 'Pythontest'},
                {'Key': 'Department', 'Value': 'Technical'},
                {'Key': 'Environment', 'Value': 'Test'}
            ]
        }
    ]
)

# Get the instance ID of the newly created instance
instance = instances[0]
instance_id = instance.id
print(f'Instance {instance_id} launched with a 20GB volume and HTTP server.')

# Stop the instance using the correct instance ID
ec2_client.stop_instances(InstanceIds=[instance_id])
print(f'Stopped the instance {instance_id}')
