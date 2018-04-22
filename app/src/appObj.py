#appObj.py - This file contains the main application object
# to be constructed by app.py

#All times will be passed to callers in UTC
# it is up to the callers to convert into any desired user timezone

from baseapp_for_restapi_backend_with_swagger import appObj
from flask_restplus import fields
from cassandraDatastore import cassandraDatastoreClass
from appParams import appParamsClass

class appObjClass(appObj):
  appParams = None
  datastore = None

  def init(self, env, testingMode = False):
    super(appObjClass, self).init(env)
    appPArams = appParamsClass(env)
    datastore = cassandraDatastoreClass('todoENVNAME','todoIPList',9000)


  def initOnce(self):
    super(appObjClass, self).initOnce()

  #override exit gracefully to stop worker thread
  def exit_gracefully(self, signum, frame):
    self.stopThread()
    super(appObjClass, self).exit_gracefully(signum, frame)

appObj = appObjClass()

