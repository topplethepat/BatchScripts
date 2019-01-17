#works with BatchUploadURL, due to lines 56 & 64
# includes metadata attachment code
# get_item adapted to get /stream for downloading URL

import requests
import json


class VoiceBaseClient:
  """Client for the VoiceBase V3 API"""

  def __init__(self, token):
    self.token = token
    self.url = 'https://apis.voicebase.com/v3'
    self.authorization_header = "Bearer " + self.token

  class VoiceBaseMedia:
    """Media class for the Voicebase V3 API Client"""
    def __init__(self, client):
      self.client = client

    def get(self):
      """Return all media"""
      pass
    def get_list(self ):
      """Get all media list"""
      headers = { 'Authorization' : self.client.authorization_header }
      response = requests.get(
        self.client.url + '/media', 
        headers = headers
      )

      return json.loads(response.text)


    def get_item(self, mediaId):
      """Get a media item"""
      headers = { 'Authorization' : self.client.authorization_header }

      response = requests.get(
        self.client.url + '/media/' + mediaId + '/streams',
        headers = headers
      )
      return json.loads(response.text)

    def delete(self, mediaId):
      """Get a media item"""
      headers = { 'Authorization' : self.client.authorization_header }

      response = requests.delete(
        self.client.url + '/media/' + mediaId,
        
        headers = headers
      )

      #print 'Response: ' + response.text
      return json.loads(response.text)

    def post(self, 
      media_url, 
      filename, 
      mime_type,
      configuration = None,
      metadata = None):

      headers = { 'Authorization' : self.client.authorization_header }
      attachments = { 
        'mediaUrl': ( 'url', media_url, 'text/url' )
      }

      if configuration is not None:
        attachments['configuration'] = ( 
          'configuration.json', configuration, 'application/json'
        )

      if metadata is not None:
        attachments['metadata'] = ( 
          'metadata.json', metadata, 'application/json'
        )  

      response = requests.post(
        self.client.url + '/media',
        headers = headers,
        files = attachments
      )
      return json.loads(response.text)

  def media(self):
    return VoiceBaseClient.VoiceBaseMedia(self)