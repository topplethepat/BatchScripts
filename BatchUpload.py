# ****** Batch Upload from csv list ******

# csv is a simple list of local file names with any directory info
# required to locate the local file - NO HEADER REQUIRED!

# command line example
#  python BatchUploadv2.py --list up.txt --mediadir .\media --results .\res.csv --token  --priority low


import argparse
import csv
import json
import os


from VoiceBaseClient import VoiceBaseClient

# ********* def main ***********
def main():
  parser = argparse.ArgumentParser(
    description = "Batch uploader to VoiceBase V3"
  )
  parser.add_argument(
    '--list', 
    help = "path to csv list of input files (one per line)", 
    required = True
  )
  parser.add_argument(
    '--mediadir',
    help = "path to local media files",
    required = False,
    default = './'
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

  upload(args.list, args.mediadir, args.results, args.token, args.priority)

# ********* def upload  ***********
def upload(list_path, mdir, results_path, token, priority):



  client = VoiceBaseClient(token = token)
  media = client.media()

  counter = 0

  with open(list_path, 'r') as list_file:
    with open(results_path, 'w') as results_file:
      results_writer = csv.writer(
        results_file, delimiter = ',', quotechar = '"'
      )

      results_writer.writerow([ 'file', 'mediaId', 'status' ]) # write headers

      for raw_filename in list_file:
        filename = raw_filename.rstrip()
        print filename

        counter = counter + 1

        pathandfile = os.path.join(mdir, filename)

        response = upload_one(media, pathandfile, filename,generate_configuration(priority))
        print response
        media_id = response['mediaId']
        status = response['status']

        results_writer.writerow([ filename, media_id, status ]);

# ********* def generate config json ***********
def generate_configuration(priority):
  return json.dumps({  
 "speechModel": {
    "features": [
        "voiceFeatures"
    ]
  }
  

})

# ********* def upload one ***********
def upload_one(media, filepath, filename, configuration):
  with open(filepath, 'r') as media_file:

    response = media.post(
      media_file, filename, 'audio/mpeg', configuration = configuration
    )

  return response

if __name__ == "__main__":
  main()