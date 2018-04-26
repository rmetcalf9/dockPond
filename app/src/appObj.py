#appObj.py - This file contains the main application object
# to be constructed by app.py

#All times will be passed to callers in UTC
# it is up to the callers to convert into any desired user timezone

from baseapp_for_restapi_backend_with_swagger import appObj as parAppObj
from flask_restplus import fields
from cassandraDatastore import name as cassandraDatastoreName, datastoreClass as cassandraDatastoreClass
from appParams import appParamsClass
from eboEndpointManager import eboEndpointManagerClass
from mainAPI import registerAPI as registerMainApi

#Test code to use local flaskbaseapp
##START DEL
from flask import Flask, Blueprint
from FlaskRestSubclass import FlaskRestSubclass
#from baseapp_for_restapi_backend_with_swagger import FlaskRestSubclass
import signal
class tmp(parAppObj):
  def init(self, env, testingMode = False):
    print('DUMMY TMP INIT')
    super(tmp, self).init(env)

  def initOnce(self):
    self.flaskAppObject = Flask(__name__)
    print('DUMMY APP OBJ USING INTERNAL FLASKRESTSUBCLASS')
    print('DUMMY APP OBJ USING INTERNAL FLASKRESTSUBCLASS')
    print('DUMMY APP OBJ USING INTERNAL FLASKRESTSUBCLASS')
    print('DUMMY APP OBJ USING INTERNAL FLASKRESTSUBCLASS')

    #Development code required to add CORS allowance in developer mode
    @self.flaskAppObject.after_request
    def after_request(response):
      if (self.globalParamObject.getDeveloperMode()):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
      return response

    api_blueprint = Blueprint('api', __name__)
    self.flastRestPlusAPIObject = FlaskRestSubclass(api_blueprint, 
      version='UNSET', 
      title='DocJob Scheduling Server API',
      description='API for the DockJob scheduling server', 
      doc='/apidocs/',
      default_mediatype='application/json'
    )
    self.flastRestPlusAPIObject.setExtraParams(
      self.globalParamObject.apidocsurl, 
      self.globalParamObject.getAPIDOCSPath(), 
      self.globalParamObject.overrideAPIDOCSPath, 
      self.globalParamObject.getAPIPath()
    )

    self.flastRestPlusAPIObject.init_app(api_blueprint)  

    self.flaskAppObject.register_blueprint(api_blueprint, url_prefix='/api')
    
    ##registerWebFrontendAPI(self) Not needed in this test
    ###self.flaskAppObject.register_blueprint(webfrontendBP, url_prefix='/frontend')
    
    signal.signal(signal.SIGINT, self.exit_gracefully)
    signal.signal(signal.SIGTERM, self.exit_gracefully) #sigterm is sent by docker stop command
##END DEL

class appObjClass(tmp):
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
    
    #Regiest main api
    registerMainApi(self)
    


  #override exit gracefully to stop worker thread
  def exit_gracefully(self, signum, frame):
    super(appObjClass, self).exit_gracefully(signum, frame)

appObj = appObjClass()

