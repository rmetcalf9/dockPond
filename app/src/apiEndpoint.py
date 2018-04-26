# Class to represent an API endpoint
#  it is used by eboEndpoint for registering the Flask API's

#from baseapp_for_restapi_backend_with_swagger import FlaskRestSubclass
from FlaskRestSubclass import FlaskRestSubclass

from flask import Blueprint
from flask_restplus import Resource
from flask import request
import datetime
import pytz

class apiEndpointClass():
  eboEndpoint = None
  flastRestPlusAPIObject = None
  docAPILocation = None
  APILocation = None

  def __init__(self, eboEndpoint):
    self.eboEndpoint = eboEndpoint
    
    self.docAPILocation = '/ebodocs/' + self.eboEndpoint.eboName + '/'
    self.APILocation = '/ebos/' + self.eboEndpoint.eboName
    
    #print('Registering EBO docs: ' + self.docAPILocation )
    api_blueprint = Blueprint('eboapi' + self.eboEndpoint.eboName, __name__)
    
    self.flastRestPlusAPIObject = FlaskRestSubclass(api_blueprint, 
      version='UNSET', 
      title='Unset',
      description='Unset', 
      doc=self.docAPILocation,
      default_mediatype='application/json'
    )
    
    caculatedUserEndpointURL = self.eboEndpoint.appObj.appParams.APIAPP_EBOAPIURL + '/' + self.eboEndpoint.eboName
    caculatedAPIDocsPath = self.eboEndpoint.appObj.appParams.getEBODOCSPath() + '/' + self.eboEndpoint.eboName
    caculatedAPIPath = self.eboEndpoint.appObj.appParams.getEBOPath() + '/' + self.eboEndpoint.eboName
    #print("1. EndpointURL: " + caculatedUserEndpointURL)
    #print("2. APIDocsPath: " + caculatedAPIDocsPath)
    #print("3. APIPath: " + caculatedAPIPath)
      
    self.flastRestPlusAPIObject.setExtraParams(
      caculatedUserEndpointURL, 
      caculatedAPIDocsPath, 
      self.eboEndpoint.appObj.appParams.overrideEBODOCSPath, 
      caculatedAPIPath
    )
    self.flastRestPlusAPIObject.init_app(api_blueprint) 
    
    try:
      self.eboEndpoint.appObj.flaskAppObject.register_blueprint(api_blueprint, url_prefix=self.APILocation)
    except:
      if not self.eboEndpoint.appObj.testingMode:
        raise
      print('Testing mode - ignoring mutiple register call for ' + self.eboEndpoint.eboName + ' EBO')
    
    self._registerAPI(self.eboEndpoint.appObj)
    
    print("*********DEBUG RULE START*************")
    for rule in self.eboEndpoint.appObj.flaskAppObject.url_map.iter_rules():
      print(rule)
    print("*********DEBUG RULE END*************")

    #raise Exception('API Endpoint init not implemented')
    
  def _registerAPI(self, appObj):
    namespace = self.flastRestPlusAPIObject.namespace('EBO', description='CRUD API\'s for EBO')
    @namespace.route('/')
    class EBOsList(Resource):
      '''Lists EBO Items'''

      @namespace.doc('getjobs')
      #@namespace.marshal_with(appObj.getResultModel(self.eboEndpoint.loadedModel))
      @appObj.flastRestPlusAPIObject.response(200, 'Success')
      @appObj.addStandardSortParams(namespace)
      def get(self):
        '''Get EBOs'''
        def outputEBO(item):
          return item.getDictForQueryMustMatchModel()
        def filterEBO(item, whereClauseText): #if multiple separated by spaces each is passed individually and anded together
          #if appObj.appData['jobsData'].jobs[item].name.upper().find(whereClauseText) != -1:
          #  return True
          #if appObj.appData['jobsData'].jobs[item].command.upper().find(whereClauseText) != -1:
          #  return True
          #return False
          return True
        return appObj.getPaginatedResult(
          appObj.eboEndpointManager.loadedEBOs,
          outputEBO,
          request,
          filterEBO
        )
    pass
    
  def unload(self):
    raise Exception('Not Implemented')
