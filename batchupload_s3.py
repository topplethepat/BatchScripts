# batch upload of local files to s3 bucket

import boto3
import csv
import os


bucketname = ''
access_key = ''
secret_key = ''

s3 = boto3.resource('s3',
					aws_access_key_id=access_key,
					aws_secret_access_key=secret_key,region_name='us-east-1'
					)
with open('up.csv', 'r') as list_file:
	list_reader = csv.DictReader(list_file, delimiter = ',')
	with open('res.csv', 'w') as results_file:
	  results_writer = csv.writer(
		results_file, delimiter = ',', quotechar = '"'
	  )
	  results_writer.writerow(['filename','s3key'])
	  for row in list_reader:
	  	filename = row['filename']

	  	my_fullpath = ''
	  	real_path = os.path.join(my_fullpath, filename)
	  	
	  	key = row['s3key'] + filename
	  	
		s3.meta.client.upload_file(real_path,bucketname,key)
		
		results_writer.writerow([filename,key])

