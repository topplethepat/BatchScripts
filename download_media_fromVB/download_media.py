#!/usr/bin/python

# gets the url from media uploaded to vb, downloads and saves it to a directory

# -*- coding: utf-8 -*-

import csv
import json
import requests
import os

from VoiceBaseClient import VoiceBaseClient

client = VoiceBaseClient(token = token)
media = client.media()

with open ('test.csv', 'r') as list_file:
	list_reader = csv.DictReader(list_file, delimiter = ',')
	for row in list_reader:
			media_id = row['mediaId']
			filename = row['externalId']
			
			saveFile = media.get_item(media_id)
			stream_url = saveFile['streams'][0]['streamLocation']
			r = requests.get(stream_url, allow_redirects=True)
			
			with open(os.path.join('./media', filename), 'wb') as ofile:
				ofile.write(r.content)

 		


