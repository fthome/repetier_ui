# repetier_ui

Une interface pour repetier serveur
(https://www.repetier-server.com)

*Repetier serveur est installé sur un raspberry pi.*

## Communication entrante:
Des gpio du raspberry pi (boutons) envoient du gcode aux imprimantes
- Extract filament
- Extrude 100mm à grande vitesse
- Extrude 50mm à petite vitesse
- STOP EMERGENCY
- HOME
- go to Z max

###Usage :

Modifier main.py
ex : 
'''HD = repetier_printer (repetier_api(api_key='my repetier API key'),'Nom de mon imprimante')
UI = repetier_ui(debug=False) #debug = True : pas d'envoie des gcode
UI.add_action(26,repetier_file_action("bip.gcode",HD))
UI.add_action(22,repetier_gcode_action("M18",HD))
'''
où 26 et 22 sont les GPIOxx utilisés.

Plans carte shield avec boutons : voir ./ELEC/


## Communication sortante:
Du gcode au niveau du serveur execute un script python qui pilote des prises IOT via IFTTT
- Coté Repetier-server : /var/lib/Repetier-Server/database/extcommands.xml 
- script : set_ifttt.py
- IFTTT : https://ifttt.com : If Maker Event "fan_on" then turn on Fan