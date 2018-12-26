#!/usr/bin/env python3

# print export for AWS_DEFAULT_REGION to a given profile
#usage: ./set_aws_region.py 

#not used anymore :)
import boto3
import os

profile_name=os.environ.get('AWS_DEFAULT_PROFILE')
region = boto3.Session(profile_name=profile_name).region_name
#we got a region or not
if region:
  print(f'export AWS_DEFAULT_REGION={region}')
else:
  print(f'echo AWS_DEFAULT_PROFILE IS_MISSING')
