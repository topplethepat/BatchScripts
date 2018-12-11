#! /usr/local/bin/python
"""
  takes a csv file list of url, eid, and base filename
  argparse lists the arguments to pass
  uploads using the url
  downloads a backup copy of the original media
"""

#  python BatchUploadURLBR.py --list ./upCIH.csv --dest CIHomedia  --results ./careinres.csv --token   --priority normal  



import argparse
import csv
import json
import requests
import os

from VoiceBaseClient import VoiceBaseClient

def main():
  parser = argparse.ArgumentParser(
    description = "Batch uploader to VoiceBase V3"
  )
  parser.add_argument(
    '--list',
    help = "path to list of input files (one per line)",
    required = True
  )

  parser.add_argument(
    '--dest',
    help = "destination directory",
    required = False,
    default = './media',
  )  

  parser.add_argument(
    '--results',
    help = "path to output csv file of files, media ids, and status",
    required = True
  )
  parser.add_argument(
    '--token',
    help = "Bearer token for V3 API authentication",
    required = True
  )
  parser.add_argument(
    '--priority',
    help = "job priority of the uploads (low, normal, high), default = low",
    required = False,
    default = 'low',
    choices = ['low', 'normal', 'high']
  )

  args = parser.parse_args()

  #check_output_path(args.dest) # create path if it does not exist

  upload(args.list, args.results, args.token, args.priority)

def upload(list_path, results_path, token, priority ):



  client = VoiceBaseClient(token = token)
  media = client.media()

  counter = 0

  with open(list_path, 'r') as list_file:
    list_reader = csv.DictReader(list_file, delimiter = ',')
    with open(results_path, 'a') as results_file:
      results_writer = csv.writer(
        results_file, delimiter = ',', quotechar = '"'
      )
      results_writer.writerow([ 'file', 'mediaId', 'status'])

      for row in list_reader:
        fileURL = row['URL']
        eid = row['externalid']
        filename = row['URL']
        #train = row[3]

        print('*** Uploading ' + str(counter) + ' ***')
        counter = counter + 1

        response = upload_one(media, fileURL, generate_configuration(priority))
        
        print response
        # if response.status_code is 200:
        #   print response
        #   media_id = response['mediaId']
        #   status = response['status']
        # else:
        #   media_id = 0
        #   status = response.status_code
        #results_writer.writerow([ fileURL, media_id, status])

def generate_configuration(priority):
  return json.dumps({
      "speechModel": {
    "features": [
        "voiceFeatures"
        
    ]
  }
  # "prediction": {
  #   "classifiers": [
  #     { "classifierId" : "" },
  #     { "classifierName": "sentiment" }
  #   ]
  # }
  })
  

def upload_one(media, fileURL, configuration):
  if fileURL.startswith('https://') or fileURL.startswith('http://'):
    print 'uploading url: ' + fileURL +'\n\n'
    # try:
    #   saveFile = requests.get(fileURL) 
    # except requests.exceptions.RequestException as e: 
    #   print('  printing error *** ' + e )

    # if saveFile.status_code == 200:


         #print 'saving file copy ' + str(len(saveFile.content))
         # with open(os.path.join(dest_path, filename), 'w') as ofile:
         #    ofile.write(saveFile.content)
    response = media.post(
            fileURL, None, None, configuration = configuration
            )
    return response
    # else:  
    #   print 'oh oh, status is:  ' + str(saveFile.status_code)
    #   return saveFile
    
  # else:
  #   with open(filename, 'r') as media_file:
  #     response = media.post(
  #       media_file, filename, 'audio/mpeg', configuration = configuration
  #     )

  # return response

def check_output_path(output_path):
  """
  test output path and create if needed
  """
  if not os.path.exists(output_path):
    os.mkdir(output_path)
  return

 

if __name__ == "__main__":
  main()
