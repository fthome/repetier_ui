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

## Communication sortante:
Du gcode au niveau du serveur execute des scripts python
- FAN ON
- FAN OFF