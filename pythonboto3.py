import boto3
ec2_resource = boto3.resource('ec2')
instances = ec2_resource.create_instances(
    ImageId = 'ami-09547c8673abb0190',
    MinCount = 1,
    MaxCount = 1,
    InstanceType = 't2.micro',
    KeyName = 'nodejskey',
    BlockDeviceMappings = [
        {
            'DeviceName': '/dev/sda1',
            'Ebs': {
                'VolumeSize': 20,  # 20 GB root volume
                'VolumeType': 'gp2',  # General Purpose SSD
                'DeleteOnTermination': False
            }
        }
    ],
    UserData='''#!/bin/bash
    # Update the package list
    sudo apt update -y
    # Install Apache
    sudo apt install apache2 -y
    # Start Apache service
    sudo systemctl start apache2
    # Enable Apache to start on boot
    sudo systemctl enable apache2
    # Create a sample index.html
    echo "<html><body><h1>Welcome to Apache Web Server - Shikhar Verma</h1></body></html>" | sudo tee /var/www/html/index.html
    # Adjust the firewall (if required)
    sudo ufw allow 'Apache'
    ''',
    TagSpecifications = [
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'Pythontest'
                },
                {
                    'Key': 'Department',
                    'Value': 'Technical',
                },
                {
                    'Key': 'Environment',
                    'Value': 'Test'
                }
            ]
        }
    ]
)

# Print instance details
for instance in instances:
    print(f'Instance {instance.id} launched with a 20GB volume and HTTP server.')

   
   
import boto3

# Create an ec2 client

ec2 = boto3.client('ec2')

# Stop the instance
instance_id = 'i-03d6aea1ba1e292c3'

ec2.stop_instances(InstanceIds=[instance_id])

print(f'Stopped the instance {instance_id}')