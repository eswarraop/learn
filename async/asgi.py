

import os
import sys


script = os.path.realpath( __file__ )
app_dir = os.path.dirname( script )
sys.path.insert(0, app_dir)

#from server import application
from q2 import app as application


if __name__ == "__main__":
    application.run()



