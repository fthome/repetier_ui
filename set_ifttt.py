# -*-coding:Utf-8 -*
import sys
import requests

sys.path.insert(0,'/home/pi')
from iftt_key import *
#key = "xxxxx"
url_base= "https://maker.ifttt.com/trigger/"

def send_cmd(cmd):
        print("Send " + cmd)
        r=requests.post(url_base+cmd+"/with/key/"+key)
        print(r.text)

send_cmd(sys.argv[1])

