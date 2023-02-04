#!/usr/bin/python3

import sys
import os

local_dir = "/home/pi/.local/lib/python3.9/site-packages"
sys.path.insert(0, local_dir)

script = os.path.realpath( __file__ )
app_dir = os.path.dirname( script )
app_dir = os.path.dirname( app_dir  )
sys.path.insert(0, app_dir)

from spaceclock import app as application


if __name__ == '__main__':
    application.run(debug=True)



