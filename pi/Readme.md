# Autostart einrichten

Folgende Datei bearbeiten

```
sudo nano /etc/rc.local
```

Dort dann vor **ecxit(0)** den Befehl eintragen
```
/home/pi/Desktop/pi/start.sh  
```
Datei ausführbar machen
```
chmod 755 start.sh
```

Neu starten und somit testen
```
sudo reboot
```