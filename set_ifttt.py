# -*-coding:Utf-8 -*
import sys
import requests

key = "mb17RKiX3cj7M0R7IxdDB0o5yIYaX3BY3dBP_CDrQ60"
url_base= "https://maker.ifttt.com/trigger/"

def send_cmd(cmd):
	print("Send " + cmd)
	r=requests.post(url_base+cmd+"/with/key/"+key)
	print(r.text)

send_cmd(sys.argv[1])
