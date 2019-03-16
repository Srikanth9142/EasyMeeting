import requests
import json

URL = 'http://www.way2sms.com/api/v1/sendCampaign'

# get request
def sendPostRequest(reqUrl, apiKey, secretKey, useType, phoneNo, senderId, textMessage):
  req_params = {
  'apikey':'WA5LUXE1YZ8B4L59BT2LJNM3U04BDI5V',
  'secret':'J83V60QCXWYR35LJ',
  'usetype':'stage',
  'phone': '9985385327',
  'message':'Hello sriku',
  'senderid':'srikanth tumpudi'
  }
  return requests.post(reqUrl, req_params)

# get response
response = sendPostRequest(URL, 'provided-api-key', 'provided-secret', 'prod/stage', 'valid-to-mobile', 'active-sender-id', 'message-text' )
"""
  Note:-
    you must provide apikey, secretkey, usetype, mobile, senderid and message values
    and then requst to api
"""
# print response if you want
print(response.text)
