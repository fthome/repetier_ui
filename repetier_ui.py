# -*-coding:Utf-8 -*

from websocket import create_connection
import json


class repetier_api(object):
	'''Un serveur Repetier pour impression 3D
	'''
	def __init__(self, host = 'localhost', port = '3344', api_key = None):
		'''Initialisation :
				- host		hostbname or IP (default : localhost)
				- port		port (default : 3344
		'''
		self.url = "ws://%s:%s/socket/"%(host, port)
		self.header = {'x-api-key': api_key}
		#TODO : test connection
		
	def send_gcode(self, printer, gcode):
		'''Send a gcode to a printer
		'''
		action = {'action': 'send', 'data': {'cmd': gcode},'printer':printer}
		ws = create_connection(self.url, header=self.header)
		ws.send(json.dumps(action))
		ws.close
		
class repetier_printer(object):
	'''Imprimante 3D reliée à REPETIER SERVEUR
	'''
	def __init__(self, repetier_serveur, name):
		'''Initialisation
				repetier_serveur	a repetier_api instance
				name				name of the printer (SLUG)
		'''
		self.name = name
		self.repetier_api = repetier_serveur
	
	def send_gcode(self, gcode):
		''' Send a gcode to the printer
		'''
		self.repetier_api.send_gcode(self.name,gcode)
	
	def send_gcode_file(self, filename):
		'''Send a gcode file to the printer
		'''
		file = open(filename,"r")
		gcode = file.read()
		self.send_gcode(gcode)
		
#EXAMPLE
if __name__=='__main__':
	HD = repetier_printer (repetier_api(api_key='142a8eed-7d86-4bea-96bc-cfcf5b3ca742'),'HD')
	HD.send_gcode("M300 P200")