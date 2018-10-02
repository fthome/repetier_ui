# -*-coding:Utf-8 -*

from repetier_ui import *

HD = repetier_printer (repetier_api(api_key='142a8eed-7d86-4bea-96bc-cfcf5b3ca742'),'HD')
HD.send_gcode("M300 P200")

#TODO : faire plus!