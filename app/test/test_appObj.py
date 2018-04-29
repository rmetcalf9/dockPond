#tests for appObj
from TestHelperSuperClass import testHelperAPIClient
import pytz
import datetime
import json
from unittest.mock import patch, call

class test_appObjClass(testHelperAPIClient):
#Actual tests below

  
  @patch('githubAPICalls.githubAPICallsClass.getEBOList', return_value=[ 'AnimalsV1', 'BandsV1', 'TownsV1' ])
  def test_CreateAppOBjInstance(self, getEBOListCall):
    self.setUpMAN()

  @patch('githubAPICalls.githubAPICallsClass.getEBOList', return_value=[ 'AnimalsV1', 'GenderV1' ])
  def test_SwaggerFilesPresent(self, getEBOListCall):
    self.setUpMAN()
    #Tests all locations for swagger files
    result = self.testClient.get('/api/swagger.json')
    self.assertEqual(result.status_code, 200, msg='/apis/swagger.json for api not present')
    result = self.testClient.get('/apidocs/swagger.json')
    self.assertEqual(result.status_code, 200, msg='/apidocs/swagger.json for apidocs not present')
    result = self.testClient.get('/ebos/GenderV1/swagger.json')
    self.assertEqual(result.status_code, 200, msg='/ebos/GenderV1/swagger.json for Gender api not present')
    result = self.testClient.get('/ebodocs/GenderV1/swagger.json')
    self.assertEqual(result.status_code, 200, msg='/ebodocs/GenderV1/swagger.json for Gender apidocs not present')
    result = self.testClient.get('/ebos/AnimalsV1/swagger.json')
    self.assertEqual(result.status_code, 200, msg='/ebos/AnimalsV1/swagger.json for Animals api not present')
    result = self.testClient.get('/ebodocs/AnimalsV1/swagger.json')
    self.assertEqual(result.status_code, 200, msg='/ebodocs/AnimalsV1/swagger.json for Animals apidocs not present')

  @patch('githubAPICalls.githubAPICallsClass.getEBOList', return_value=[ 'AnimalsV1', 'GenderV1' ])
  def test_docsIndexesPresent(self, getEBOListCall):
    self.setUpMAN()
    #Tests all locations for swagger files
    result = self.testClient.get('/apidocs/')
    self.assertEqual(result.status_code, 200, msg='/apidocs/ not present')
    result = self.testClient.get('/ebodocs/GenderV1/')
    self.assertEqual(result.status_code, 200, msg='/ebodocs/GenderV1/ not present')
    result = self.testClient.get('/ebodocs/AnimalsV1/')
    self.assertEqual(result.status_code, 200, msg='/ebodocs/AnimalsV1/ not present')
    
    #Requires trailing slash
    #result = self.testClient.get('/apidocs')
    #self.assertEqual(result.status_code, 200, msg='/apidocs not present')
    #result = self.testClient.get('/ebodocs/GenderV1')
    #self.assertEqual(result.status_code, 200, msg='/ebodocs/GenderV1 not present')
    #result = self.testClient.get('/ebodocs/AnimalsV1')
    #self.assertEqual(result.status_code, 200, msg='/ebodocs/AnimalsV1 not present')
