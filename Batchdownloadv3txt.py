#  batch txt download
# takes out unicode characters
## example command line
# python BatchDownloadv3txt.py --outstanding ./outstanding.csv --results ./res.csv --output ./json --token  ****token goes here****  



import argparse
import csv
import json
import os
import io


from VoiceBaseClient import VoiceBaseClient

def main():
	parser = argparse.ArgumentParser(
		description = 'Batch downloader to VoiceBase V3 for txt format'
	)
	parser.add_argument(
		'--results', 
		help = 'path to download list, or upload result csv file of files, media ids, and status',
		# this is the list to upload, has header: file mediaId status
		required = True
	)
	parser.add_argument(
		'--outstanding',
		help = 'path to csv file of outstanding (not finished) files',
		# saving the portion of the list that is not yet ready
		required = True
	)
	parser.add_argument(
		'--output',
		help = 'path to directory to write outputs',
		required = True
	)
	parser.add_argument(
		'--token',
		help = 'Bearer token for V3 API authentication',
		required = True
	)


	args = parser.parse_args()

	download(
		args.results, 
		args.outstanding,
		args.output,
		args.token
	)

def download(results_path, outstanding_path, output_path, token):


	client = VoiceBaseClient(token = token)
	media = client.media()

	with open(results_path, 'r') as results_file:
		results_reader = csv.DictReader(results_file)
		
		
		with open(outstanding_path, 'w') as outstanding_file:
			outstanding_writer = csv.writer(
				outstanding_file, delimiter = ',', quotechar = '"'
			)
			outstanding_writer.writerow([ 'file', 'mediaId', 'status' ])
			
			for results_row in results_reader:
				filename = results_row['file']
				media_id = results_row['mediaId']
				
				if len(media_id)  < 10:  # expected len 36, 0 is the failure condition  bail out if mediID is  not correct length - had a blank row problem in csv
					continue
				original_status = results_row['status']

				api_results = media.get_item(media_id)
				print api_results
				if 2<3: 
						write_txtresult_to_output(output_path, filename, api_results)
				

def write_txtresult_to_output(output_path, filename, results):
	if not os.path.exists(output_path):
		os.mkdir(output_path)
	with io.open(os.path.join(output_path,  (os.path.splitext(os.path.basename(filename))[0] + '.txt')), 'w', encoding='utf8') as output_file:
		output_file.write(results)  


if __name__ == "__main__":
	main()