# batch download for media stored in s3 bucket

import boto3
import botocore
import csv
import json
import requests
import os

def download_file_with_client(access_key, secret_key, bucket_name, key, local_path):
    client = boto3.client('s3',
                            aws_access_key_id=access_key,
                            aws_secret_access_key=secret_key,region_name='us-east-1',
                            )
    client.download_file(bucket_name, key, local_path)
    
    
counter = 0
access_key = ''
secret_key = ''
bucket_name = ''

with open('.csv','r') as list_file:
	list_reader = csv.DictReader(list_file, delimiter = ',')
	for row in list_reader:
			key = row['s3key']
			#print key
			local_path = key[62:] #gets last part of key as filename
			
			download_file_with_client(access_key, secret_key, bucket_name, key, local_path)
			print counter
			counter += 1