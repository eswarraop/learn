#!/usr/bin/python3

import sys
import os

local_dir = "/home/pi/.local/lib/python3.9/site-packages"
sys.path.insert(0, local_dir)

app_dir = os.path.dirname( os.getcwd())
sys.path.insert(0, app_dir)

from spaceclock import app as application


if __name__ == '__main__':
    application.run(debug=True)



