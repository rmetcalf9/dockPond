#appObj.py - This file contains the main application object
# to be constructed by app.py

#All times will be passed to callers in UTC
# it is up to the callers to convert into any desired user timezone

from baseapp_for_restapi_backend_with_swagger import appObj
from flask_restplus import fields
from cassandraDatastore import name as cassandraDatastoreName, datastoreClass as cassandraDatastoreClass
from appParams import appParamsClass
from eboEndpointManager import eboEndpointManagerClass

class appObjClass(appObj):
  appParams = None
  datastore = None
  eboEndpointManager = None

  def init(self, env, testingMode = False):
    super(appObjClass, self).init(env)
    self.appParams = appParamsClass(env)
    self.datastore = cassandraDatastoreClass(self.appParams.APIAPP_ENVIROMENT,env)
    
    print('Starting dockPond')
    print ('\nDuckPond vars:')
    self.appParams.printVarValues()
    print ('\nDatastore vars:')
    self.datastore.printVarValues()
    print ('\nMain vars:')
    
    self.datastore.initStore()

    self.eboEndpointManager = eboEndpointManagerClass(self)
    self.eboEndpointManager.scanGitandLoadEBOs()

  def initOnce(self):
    super(appObjClass, self).initOnce()

  #override exit gracefully to stop worker thread
  def exit_gracefully(self, signum, frame):
    super(appObjClass, self).exit_gracefully(signum, frame)

appObj = appObjClass()

