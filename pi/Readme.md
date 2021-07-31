# Autostart einrichten

Folgende Datei bearbeiten

```
sudo nano /etc/rc.local
```

Dort dann vor **ecxit(0)** den Befehl eintragen
```
/Desktop/pi/start.sh  
```
Neu starten und somit testen
```
sudo reboot
```