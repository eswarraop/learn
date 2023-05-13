#!/bin/bash

sudo curl -X PUT --data-binary '{
  "listeners": {
      "*:80": {
          "pass": "applications/spaceclock_asgi"
      }
  },
  "applications": {
      "spaceclock_asgi": {
          "processes": 2,
          "limits": {
              "timeout": 3,
              "requests": 500

          },
          "type": "python",
          "path": "/home/pi/learn/async/",
          "module": "asgi"
      }
  }
  }' --unix-socket /usr/local/var/run/unit/control.unit.sock http://10.0.0.10/config/

