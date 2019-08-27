# ****** Batch Upload to align human transcripts from directory ******

# command line example
#  python batchalignerupload.py --list  --transcriptdir ./ --priority 
#  

import argparse
import csv
import json
import os
import io
import requests


token = 'your_vb_token'

# ********* def main ***********
def main():
	parser = argparse.ArgumentParser(
		description = "Batch aligner to VoiceBase V3"
	)
	parser.add_argument(
		'--list', 
		help = "path to csv list of input files (one per line)", 
		required = True
	)
	parser.add_argument(
		'--transcriptdir',
		help = "path to local transcript files",
		required = False,
		default = './'
	)

	parser.add_argument(
		'--priority',
		help = "job priority of the uploads (low, normal, high), default = low",
		required = False,
		default = 'low',
		choices = ['low', 'normal', 'high']
	)

	args = parser.parse_args()

	upload(args.list, args.transcriptdir, args.priority)

# ********* def upload  ***********
def upload(list_path, transcriptdir, priority):


	counter = 0

	with open(list_path, 'r') as list_file:
		list_reader = csv.DictReader(list_file)
			
		#for file in os.listdir(transcriptdir):
			#if file.endswith('.txt'):

		for row in list_reader:
			try:
				filename = row['filename']
				file = filename[0:9] + ".txt"
				media_id = row['mediaId']				
				#if file.endswith('.txt'):
				file_path = os.path.join(transcriptdir, file)
				print file_path
				
				mdx = {
					"externalId": filename,
					"extended": {
					 "score": 0,
					"information": {
					"sampleKey": 1
					},
					"modelTargets": {}
					}
					}

				m_data = json.dumps(mdx)
				data = {'metadata': m_data}
				files={'transcript': open(file_path, 'rb'), 'Content-Type': 'form-data'}
				response = requests.post(
					'https://apis.voicebase.com/v3/media/' + media_id,
						headers = { 'Authorization' : "Bearer " + token },
						files = files, data = data
						)
					
				counter += 1
				print counter
				with open('aligner_res.csv','a') as results_file:
					results_writer = csv.writer(
					results_file, delimiter = ',', quotechar = '"'
	  				)
	  				
					results_writer.writerow([ filename, media_id])
			except IOError:
				print "moving on"
				

if __name__ == "__main__":
	main()