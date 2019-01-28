# -*-coding:Utf-8 -*
import sys
import requests


class ifttt(object):
    '''Classe pour actions IFTTT
    '''
    def __init__(self, key, url= "https://maker.ifttt.com/trigger/"):
        self.url_base = url
        self.key = key
    def send_cmd(self, cmd):
        '''Send the Cmd on IFTTT
        '''
        print("Send " + cmd)
        r=requests.post(self.url_base+cmd+"/with/key/"+self.key)
        print(r.text)

if __name__ == "__main__":
    sys.path.insert(0,'/home/pi')
    from iftt_key import *
    ifttt0 = ifttt(key)
    ifttt0.send_cmd(sys.argv[1])
