# -*-coding:Utf-8 -*

from repetier_ui import *
import time
import set_ifttt

from FUTIL.my_logging import *

my_logging(console_level = DEBUG, logfile_level = INFO)

HD = repetier_printer (repetier_api(api_key='142a8eed-7d86-4bea-96bc-cfcf5b3ca742'),'HD')

sys.path.insert(0,'/home/pi')
import iftt_key
ifttt0 = set_ifttt.ifttt(iftt_key.key)

UI = repetier_ui(debug=False, wake_up = lambda x: iftt.send_cmd("HD_on")) #debug = True : pas d'envoie des gcode
UI.add_action(22,repetier_file_action("extract.gcode",HD))
UI.add_action(27,repetier_file_action("extrude_100_vite.gcode",HD))
UI.add_action(17,repetier_file_action("extrude_50.gcode",HD))
UI.add_action(10,repetier_file_action("goto_z_max.gcode",HD))
UI.add_action(19,repetier_file_action("stop_all.gcode",HD))
UI.add_successive_actions(26,repetier_file_action("pause.gcode",HD), repetier_action_action("continueJob",HD))



try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    print('interrupted!')
finally:
	UI.close()
