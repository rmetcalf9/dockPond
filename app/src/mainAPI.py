from flask_restplus import Resource
from flask import request
import datetime
import pytz
from eboEndpoint import getEBOModel
from werkzeug.exceptions import BadRequest

def registerAPI(appObj):
  nsMain = appObj.flastRestPlusAPIObject.namespace('EBOs', description='Information about EBOs loaded')
  @nsMain.route('/')
  class EBOsList(Resource):
    '''Lists loaded EBOs'''

    @nsMain.doc('getEBOs')
    @nsMain.marshal_with(appObj.getResultModel(getEBOModel(appObj)))
    @appObj.flastRestPlusAPIObject.response(200, 'Success')
    @appObj.addStandardSortParams(nsMain)
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

  @nsMain.route('/requestReload')
  class APIFunctions(Resource):
    '''API Admin functions'''

    @nsMain.doc('requestReload')
    ##@nsMain.marshal_with(appObj.getResultModel(getEBOModel(appObj)))
    @appObj.flastRestPlusAPIObject.response(200, 'Success')
    def get(self):
      '''request Reload of APIs from guthub'''
      return appObj.watcherThread.requestReload()

