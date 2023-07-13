#!/bin/bash

sudo curl -X GET --unix-socket /var/run/control.unit.sock http://10.0.0.20:8192/control/applications/spaceclock_asgi/restart
sudo curl -X GET --unix-socket /var/run/control.unit.sock http://10.0.0.20:8192/config
sudo curl -X PUT --data-binary @config.json --unix-socket /var/run/control.unit.sock http://10.0.0.20/config/

