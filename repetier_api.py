# -*-coding:Utf-8 -*

import requests


api_key = '142a8eed-7d86-4bea-96bc-cfcf5b3ca742'

#test
r=requests.get("http://localhost:3344/printer/info")
print(r.text)

params = {'apikey':api_key}
r=requests.get("http://localhost:3344/printer/log/HD",params=payload)

params['a']='listPrinter'
r=requests.get("http://localhost:3344/printer/api/HD",params=params)
t.text

headers = {'x-api-key': api_key}
params = {'a': 'send', 'data': {'cmd': 'M300 P300'}}

r=requests.get("http://localhost:3344/printer/api/HD",params=params, headers=headers)


#import websocket
from websocket import create_connection
api_key = '142a8eed-7d86-4bea-96bc-cfcf5b3ca742'
header = {'x-api-key': api_key}
url = "ws://localhost:3344/socket/"
ws = create_connection(url, header=header)
ws.send('{"action":"send","data":{"cmd":"M300 P300"},"printer":"HD","callback_id":545}')

#ou
import json
action = {'action': 'send', 'data': {'cmd': 'M300 P300'},'printer':'HD'}
ws = create_connection(url, header=header)
ws.send(json.dumps(action))
ws.close
