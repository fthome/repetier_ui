# -*-coding:Utf-8 -*

from websocket import create_connection
import json
import RPi.GPIO as GPIO
import logging
import time
import requests


# NOTES : il y aurait surement à simplifier la gestion du débounce!
#TODO : gestion des appuis longs
#TODO : faire des boutons de type on-off (ex : pause / continue)

class repetier_api(object):
	'''Un serveur Repetier pour impression 3D
	'''
	def __init__(self, host = 'localhost', port = '3344', api_key = None):
		'''Initialisation :
				- host		hostname or IP (default : localhost)
				- port		port (default : 3344
		'''
		self.ws_url = "ws://%s:%s/socket/"%(host, port)
		self.header = {'x-api-key': api_key}
		self.api_key = api_key
		#TODO : test connection
		self.api_url = "http://%s:%s/printer/api/" % (host, port)
		"http://localhost:3344/printer/api/<slug>?a=<websocket command>&data=<json object properly url-escaped>&apikey=<API key>>"
		
	def send_gcode(self, printer, gcode):
		'''Send a gcode to a printer
		'''
		datas = {'a': 'send', 'data': {'cmd': gcode}}
		self.send(printer, datas)
		logging.debug("GCODE : %s"%(json.dumps(datas)))
	
	def send_action(self, printer, action):
		'''Send a action to the printer (ex : action="continueJob")
		'''
		datas = {'a': action, 'data': {}}
		self.send(printer , datas)
		logging.debug("ACTION : %s"%(json.dumps(datas)))
	
	def ws_send(self, datas):
		'''Send via websockets (depreciate)
		'''
		try:
			ws = create_connection(self.ws_url, header=self.header)
			ws.send(json.dumps(datas))
		except Exception as e:
			logging.error("WebsocketError: %s"%(err.message))
		finally:
			ws.close	
			
	def send(self, printer, action, datas):
		'''Send then command by api
		'''
		url = self.url + printer 
		#datas['apikey']=self.api_key
		r = request.post(url, data = datas, headers=self.header)
		logging.info("HTTP response : %s"%(r.text))
		
		
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
		try:
			file = open(filename,"r")
			gcode = file.read()
			self.send_gcode(gcode)
		except IOError:
			logging.error("File not found : %s"%(filename))
	def send_action(self, action):
		'''Send a action to the printer (ex : action="continueJob")
		'''
		self.repetier_api.send_action(self.name,action)
		
class repetier_ui(object):
	''' Un raspberry pi avec des boutons qui lancent des actions sur le serveur repetier
	'''
	def __init__(self, bounce_time = 1000, debug=False):
		'''Initialisation
		'''
		self.actions = {}
		self.current_action = {}
		self.debug = debug
		self.bounce_time = bounce_time
		self.last_action_time = time.time()
		GPIO.setmode(GPIO.BCM)
		logging.info("Repetier UI started.")
		if debug:
			logging.info("Debug mode is on : gcode are not send.")
	
	def add_action(self, pin, action):
		'''Add an action when the gpio pin is down
		'''
		self.actions[pin]=action
		action.repetier_ui = self
		if self.debug:
			action.set_debug_mode(True)
		GPIO.setup(pin,GPIO.IN)
		GPIO.add_event_detect(pin, GPIO.FALLING, callback=self.actions[pin].execute, bouncetime= self.bounce_time)
	
	def add_successive_actions(self, pin, *actions):
		'''Add  actions who are successively done:
			1st push : action 1
			2nd push : action 2
			...
			n push : action 1
		'''
		self.actions[pin] = actions
		self.current_action[pin] = 0
		for action in actions:
			action.repetier_ui = self
			if self.debug:
				action.set_debug_mode(True)
		GPIO.setup(pin,GPIO.IN)
		GPIO.add_event_detect(pin, GPIO.FALLING, callback=self.successive_action(pin), bouncetime= self.bounce_time)
		
	def successive_action(self, pin):
		'''Return a callback function for add_event_detect
		'''
		callback = self.actions[pin][self.current_action[pin]].execute
		self.current_action[pin] = (self.current_action[pin] + 1) % len(self.actions[pin])
		return callback
	
	def close(self):
		'''Close interface
		'''
		logging.info("Repetier UI closed.")
		GPIO.cleanup()  
		
	def not_bounce(self, channel):
		''' Return False if another action is runnig before bource_time
			or channel GPIO is not LOW
		'''
		if GPIO.input(channel)==0:
			now = time.time()
			if now - self.last_action_time > self.bounce_time/1000.0:
				self.last_action_time = now
				return True

class repetier_action(object):
	'''Une action à réaliser sur une imprimante
	'''
	def __init__(self, printer, debug = False):
		self.printer = printer
		self.debug = debug
		
	def set_debug_mode(self, debug):
		''' Set debug mode on/off (debug = no gcoden sent)
		'''
		self.debug = debug

		
		
class repetier_gcode_action(repetier_action):
	'''Une action à base string (=gcode)
	'''
	def __init__(self, gcode, printer, debug = False):
		'''Initialisation
			gcode	:		string of gcode ex : "M300 S1000"
			printer	:		a repetier_printer object
		'''
		self.gcode = gcode
		repetier_action.__init__(self, printer, debug)
		
	def execute(self, channel):
		'''Execute the gcode on the printer
		'''
		if self.repetier_ui.not_bounce(channel):
			logging.info("GPIO%s FALLING => GCODE : %s send to %s."%(channel, self.gcode, self.printer.name))
			if not self.debug:
				self.printer.send_gcode(self.gcode)
		
class repetier_file_action(repetier_action):
	'''Une action à base de fichier contenant du gcode
	'''
	def __init__(self, filename, printer, debug = False):
		'''Initialisation
			file_name	:		name of the file with gcode
			printer		:		a repetier_printer object
		'''
		self.filename = filename
		repetier_action.__init__(self, printer, debug)
		
	def execute(self, channel):
		'''Execute the gcode on the printer
		'''
		if self.repetier_ui.not_bounce(channel):
			logging.info("GPIO%s FALLING => GCODE : %s send to %s."%(channel, self.filename, self.printer.name))
			if not self.debug:
				self.printer.send_gcode_file(self.filename)				
		
class repetier_action_action(repetier_action):
	'''Une action simple (ex : "continueJob")
	'''
	def __init__(self, action, printer, debug=False):
		'''Initialisation
			action		:		action (string)
			printer		:		a repetier_printer object
		'''
		self.action = action
		repetier_action.__init__(self, printer, debug)
	
	def execute(self, channel):
		'''Execute the action on the printer
		'''
		if self.repetier_ui.not_bounce(channel):
			logging.info("GPIO%s FALLING => ACTION : %s send to %s."%(channel, self.action, self.printer.name))
			if not self.debug:
				self.printer.send_action(self.action)				
		
		
#EXAMPLE
if __name__=='__main__':
	import sys
	HD = repetier_printer (repetier_api(api_key='142a8eed-7d86-4bea-96bc-cfcf5b3ca742'),'HD')
	HD.send_gcode_file(sys.argv[1])