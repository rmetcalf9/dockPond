# Class to represent an API endpoint
#  it is used by eboEndpoint for registering the Flask API's

from baseapp_for_restapi_backend_with_swagger import FlaskRestSubclass

from flask import Blueprint
from flask_restplus import Resource
from flask import request
import datetime
import pytz

from werkzeug.exceptions import BadRequest

from flask_restplus import fields

eboKeyNotFoundMessage = 'EBO Key not found'

def getGetModelFunctionFromPythonFile(pythonFile):
  ldict = locals()
  exec(pythonFile, None,ldict)
  return ldict['getModel']

class apiEndpointClass():
  eboEndpoint = None
  flastRestPlusAPIObject = None
  docAPILocation = None
  APILocation = None

  EBOModel = None

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
    
    getModelFN = getGetModelFunctionFromPythonFile(self.eboEndpoint.pythonFile)
    if getModelFN is None:
      raise Exception('Failed to load model - (getModel = None)')

    self.EBOModel = getModelFN(self.flastRestPlusAPIObject)

    self.eboEndpoint.appObj.datastore.initObjectType(self.eboEndpoint.eboName)
    self._registerAPI(self.eboEndpoint.appObj)
    
    #print("*********DEBUG RULE START*************")
    #for rule in self.eboEndpoint.appObj.flaskAppObject.url_map.iter_rules():
    #  print(rule)
    #print("*********DEBUG RULE END*************")
    
  def _registerAPI(self, appObj):
    datastore = appObj.datastore
    objectTypeName = self.eboEndpoint.eboName
    namespace = self.flastRestPlusAPIObject.namespace('EBO', description='CRUD API\'s for EBO')
    @namespace.route('/')
    class EBOsList(Resource):
      '''Lists EBO Items'''

      @namespace.doc('getlist')
      @namespace.marshal_with(appObj.getForiegnResultModel(self.EBOModel, self.flastRestPlusAPIObject))
      @self.flastRestPlusAPIObject.response(200, 'Success')
      @appObj.addStandardSortParams(namespace)
      def get(self):
        '''Get EBOs'''
        def outputEBO(item):
          return item
        def filterEBO(item, whereClauseText): #Queries must be implemented by datastore
          return True

        offset = request.args.get('offset')
        if offset is None:
          offset = 0
        else:
          offset = int(offset)
        pagesize = request.args.get('pagesize')
        if pagesize is None:
          pagesize = 100
        else:
          pagesize = int(pagesize)

        return appObj.getPaginatedResult(
          datastore.queryList(objectTypeName, None, None, pagesize, offset),
          outputEBO,
          request,
          filterEBO
        )

    @namespace.route('/<string:key>')
    @namespace.response(400, eboKeyNotFoundMessage)
    @namespace.param('key', 'EBO key')
    class job(Resource):
      '''Show a EBO'''
      @namespace.doc('get_EBO')
      @namespace.marshal_with(self.EBOModel)
      def get(self, key):
        '''Fetch a given EBO'''
        try:
          retVal = datastore.query(objectTypeName, key)
          return retVal
        except:
          raise BadRequest(eboKeyNotFoundMessage)
        return None

      @namespace.doc('delete_ebo')
      @namespace.response(200, 'EBO deleted')
      @namespace.response(400, eboKeyNotFoundMessage)
      def delete(self, key):
        '''Delete EBO'''
        deletedEBO = dict()
        deletedEBO['ABC'] = '123'
        #deletedEBO = None
        try:
          #deletedEBO = appObj.appData['jobsData'].getJobByName(guid)
          raise Exception('Delete not implemented')
          pass
        except:
          raise BadRequest(eboKeyNotFoundMessage)
        ##appObj.appData['jobsData'].deleteJob(deletedJob)
        return deletedJob

      @namespace.doc('upsert_ebo')
      @namespace.expect(self.EBOModel, validate=True)
      @namespace.response(200, 'EBO Upserted')
      @namespace.response(400, 'Validation Error')
      @appObj.flastRestPlusAPIObject.marshal_with(self.EBOModel, code=200, description='EBO upserted')
      def put(self, key):
        '''Upsert EBO'''
        retData = datastore.upsert(objectTypeName, key, request.get_json())
        return retData


  def unload(self):
    raise Exception('Not Implemented')
