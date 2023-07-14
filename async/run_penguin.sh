#!/bin/bash

sudo curl -X GET --unix-socket /var/run/control.unit.sock http://localhost/control/applications/spaceclock_asgi/restart
sudo curl -X GET --unix-socket /var/run/control.unit.sock http://localhost/config
sudo curl -X PUT --data-binary @config.json --unix-socket /var/run/control.unit.sock http://localhost/config/

