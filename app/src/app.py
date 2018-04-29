from appObj import getAppObj

import sys
import os
import watcherThread

##App will host content in the following paths:
## /api        API
## /apidocs    API Documentation including swagger.json and swaggerUI
## /frontend   Frontend for this application
##
## for EBOs:
## /ebos/AnimalsV1/
## /ebodocs/AnimalsV1/

watcherThread = watcherThread.watcherThreadClass()
watcherThread.start()

getAppObj().init(os.environ, watcherThread)

expectedNumberOfParams = 0
if ((len(sys.argv)-1) != expectedNumberOfParams):
  raise Exception('Wrong number of paramaters passed (Got ' + str((len(sys.argv)-1)) + " expected " + str(expectedNumberOfParams) + ")")

getAppObj().run()

watcherThread.stopThreadRunning()
watcherThread.join()


