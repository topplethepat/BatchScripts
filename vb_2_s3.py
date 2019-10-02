# gets streaming URL for each file from VB, 
# uploads to s3 bucket

import csv
import json
import os
import boto3
import boto3.session

from botocore.client import Config
from VoiceBaseClient import VoiceBaseClient


access_key = ''
secret_key = ''

s3 = boto3.resource('s3',
					aws_access_key_id=access_key,
					aws_secret_access_key=secret_key,region_name='us-east-1'
					)


client = VoiceBaseClient(token = '')

with open('list.csv', 'r') as list_file:
	list_reader = csv.DictReader(list_file, delimiter = ',')
	for row in list_reader:
		media_id = row['mediaId']
		external_id = row['externalId']
		with open('res.csv', 'a') as results_file:
			file_is_empty = os.stat('res.csv').st_size == 0
			results_writer = csv.writer(
			results_file, delimiter = ',', quotechar = '"'
			)
			if file_is_empty:
				results_writer.writerow(['fileURL','key', 'mediaId','externalId'])
			
			key = 'example_key'
			bucketname = 'somebucket'
			
			media_stream = media.get_item(media_id)
			stream_url = media_stream['streams'][0]['streamLocation']
		
			my_object = s3.Object(bucketname, key)
			my_object.put(Body=stream_url)
			results_writer.writerow([stream_url,key,media_id,external_id])


