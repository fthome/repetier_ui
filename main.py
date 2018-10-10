# -*-coding:Utf-8 -*

from repetier_ui import *
import time

from FUTIL.my_logging import *

my_logging(console_level = DEBUG, logfile_level = INFO)

HD = repetier_printer (repetier_api(api_key='142a8eed-7d86-4bea-96bc-cfcf5b3ca742'),'HD')

UI = repetier_ui()
UI.add_action(22,repetier_file_action("extract.gcode",HD))
UI.add_action(27,repetier_file_action("extrude_100_vite.gcode",HD))
UI.add_action(17,repetier_file_action("extrude_50.gcode",HD))

try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    print('interrupted!')
finally:
	UI.close()