# Copyright is waived. No warranty is provided. Unrestricted use and modification is permitted.

import sys

try:
    import boto3
    from botocore.config import Config
except ImportError:
    sys.exit('Requires Boto3 module; try "pip install boto3"')

PURPOSE = '''\
List Amazon Linux 2 images in specified region

amazon-linux2-images.py <region>
'''

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(PURPOSE)
    region = sys.argv[1]
    ec2 = boto3.client('ec2', config=Config(region_name=region))
    response = ec2.describe_images(
        Filters=[
            {'Name': 'architecture', 'Values': ['x86_64']},
            {'Name': 'block-device-mapping.volume-type', 'Values': ['gp2']},
            {'Name': 'description', 'Values': ['Amazon Linux 2 AMI*', 'Amazon Linux 2 Kernel*']},
            {'Name': 'state', 'Values': ['available']},
            {'Name': 'virtualization-type', 'Values': ['hvm']},
        ],
        Owners=["amazon"]
    )
    for image in reversed(sorted(response['Images'], key=lambda x: x['CreationDate'])):
        print('{0} {1} {2}'.format(image['ImageId'], image['CreationDate'], image['Description']))
