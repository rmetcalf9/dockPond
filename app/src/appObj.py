#appObj.py - This file contains the main application object
# to be constructed by app.py

#All times will be passed to callers in UTC
# it is up to the callers to convert into any desired user timezone

from baseapp_for_restapi_backend_with_swagger import AppObjBaseClass as parAppObj
from flask_restplus import fields
from cassandraDatastore import name as cassandraDatastoreName, datastoreClass as cassandraDatastoreClass
from appParams import appParamsClass
from eboEndpointManager import eboEndpointManagerClass
from mainAPI import registerAPI as registerMainApi

class appObjClass(parAppObj):
  appParams = None
  datastore = None
  eboEndpointManager = None
  
  testingMode = False

  def init(self, env, testingMode = False):
    super(appObjClass, self).init(env)
    self.testingMode = testingMode #Causes APIs to only register if they are not already registered
    
    self.appParams = appParamsClass(env)
    self.datastore = cassandraDatastoreClass(self.appParams.APIAPP_ENVIROMENT,env)
    
    print('Starting dockPond')
    print ('\nDockPond vars:')
    self.appParams.printVarValues()
    print ('\nDatastore vars:')
    self.datastore.printVarValues()
    print ('\nMain vars:')
    
    self.datastore.initStore()

    self.eboEndpointManager = eboEndpointManagerClass(self)
    self.eboEndpointManager.scanGitandLoadEBOs()

  def initOnce(self):
    super(appObjClass, self).initOnce()
    
    #Regiest main api
    registerMainApi(self)
    


  #override exit gracefully to stop worker thread
  def exit_gracefully(self, signum, frame):
    super(appObjClass, self).exit_gracefully(signum, frame)

  #Get a result model but for a different flaskRestPLus API
  # todo move this into base app
  def getForiegnResultModel(self, recordModel, restPlusAPI):
    paginationModel = restPlusAPI.model('paginationList', {
      'offset': fields.Integer(default='0',description='Number to start from'),
      'pagesize': fields.Integer(default='',description='Results per page'),
      'total': fields.Integer(default='0',description='Total number of records in output')
    })
    return restPlusAPI.model('resultList', {
      'pagination': fields.Nested(paginationModel),
      'result': fields.List(fields.Nested(recordModel)),
    })


appObj = appObjClass()

