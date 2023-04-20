

import uvicorn
import os
import sys


script = os.path.realpath( __file__ )
app_dir = os.path.dirname( script )
#app_dir = os.path.dirname( app_dir  )
sys.path.insert(0, app_dir)



config = uvicorn.Config("q2:app", host='10.0.0.10', port=5000, 
            log_level="info", loop='uvloop', http='httptools',
            limit_concurrency=10, limit_max_requests=8192)

application = uvicorn.Server(config)


