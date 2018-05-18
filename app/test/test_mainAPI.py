from TestHelperSuperClass import testHelperAPIClient
import unittest
import json
from unittest.mock import patch, call

model_str = "from flask_restplus import fields\n\ndef getModel(flaskRestPlusAPI):\n  return flaskRestPlusAPI.model('Animal', {\n      'name': fields.String(default='',description='What is the name of this animal? (Must be unique)')\n  })"

class test_mainAPI(testHelperAPIClient):

  @patch('githubAPICalls.githubAPICallsClass.getEBOList', return_value=[ 'AnimalsV1', 'BandsV1', 'TownsV1' ])
  @patch('githubAPICalls.githubAPICallsClass.getEBOInfoFileFromGit', return_value='{"Deployments": {"DEV_INT_TEST": "0.0.1"}}')
  @patch('githubAPICalls.githubAPICallsClass.getEBOInfoFileFromGit', return_value='{"Deployments": {"DEV_INT_TEST": "0.0.1"}}')
  @patch('githubAPICalls.githubAPICallsClass.getEBOInfoFileFromGit', return_value='{"Deployments": {"DEV_INT_TEST": "0.0.1"}}')
  @patch('githubAPICalls.githubAPICallsClass.getPythonModelFileFromGit', return_value=model_str)
  @patch('githubAPICalls.githubAPICallsClass.getPythonModelFileFromGit', return_value=model_str)
  @patch('githubAPICalls.githubAPICallsClass.getPythonModelFileFromGit', return_value=model_str)
  def test_getEBOs(self, getEBOListCall, getEBOInfoFileFromGit1, getEBOInfoFileFromGit2, getEBOInfoFileFromGit3, getPythonModelFileFromGit1, getPythonModelFileFromGit2, getPythonModelFileFromGit3):
    self.setUpMAN()
    expRes = {
      "pagination": {
        "offset": 0, "pagesize": 100, "total": 3
       }, 
       "result": [
        {"name": "TownsV1"}, {"name": "AnimalsV1"}, {"name": "BandsV1"}
       ]
      }
    result = self.testClient.get('/api/EBOs/')
    self.assertEqual(result.status_code, 200)
    resultJSON = json.loads(result.get_data(as_text=True))
    self.assertJSONStringsEqual(resultJSON['pagination'], expRes['pagination'], msg="Pagination part wrong")
    matchedARR = list(expRes['result'])
    numMatched = 0
    for returnedIdx, returnedVal in enumerate(resultJSON['result']):
      for idx, val in enumerate(matchedARR):
        # print(val['name'])
        # print(returnedVal['name'])
        if val['name'] == returnedVal['name']:
          matchedARR[idx] = {"name": "_"}
          numMatched = numMatched + 1
          print(returnedVal['errorStateReason'])
          self.assertEqual(returnedVal['state'],'OK', msg=returnedVal['name'] + ' API found but state != OK (it was ' + returnedVal['state'] + ')')
    self.assertEqual(len(matchedARR),numMatched,msg='Didn\'t match all results')
    
  #Swagger files tested in appObj


  @patch('githubAPICalls.githubAPICallsClass.getEBOList', return_value=[ 'AnimalsV1', 'BandsV1', 'TownsV1' ])
  @patch('githubAPICalls.githubAPICallsClass.getEBOInfoFileFromGit', return_value='{"Deployments": {"DEV_INT_TEST": "0.0.1"}}')
  @patch('githubAPICalls.githubAPICallsClass.getEBOInfoFileFromGit', return_value='{"Deployments": {"DEV_INT_TEST": "0.0.1"}}')
  @patch('githubAPICalls.githubAPICallsClass.getEBOInfoFileFromGit', return_value='{"Deployments": {"DEV_INT_TEST": "0.0.1"}}')
  @patch('githubAPICalls.githubAPICallsClass.getPythonModelFileFromGit', return_value=model_str)
  @patch('githubAPICalls.githubAPICallsClass.getPythonModelFileFromGit', return_value=model_str)
  @patch('githubAPICalls.githubAPICallsClass.getPythonModelFileFromGit', return_value=model_str)
  def test_ebodocs_redirect_bad_URLs(self, getEBOListCall, getEBOInfoFileFromGit1, getEBOInfoFileFromGit2, getEBOInfoFileFromGit3, getPythonModelFileFromGit1, getPythonModelFileFromGit2, getPythonModelFileFromGit3):
    self.setUpMAN()
    result = self.testClient.get('/ebodocs/AnimalsV1')
    self.assertEqual(result.status_code, 301)
    self.assertEqual(result.headers['location'], 'http://localhost:3033/ebodocs/AnimalsV1/')

    #/ebos/ is never registered so will never redirect badly
    #result = self.testClient.get('/ebos/AnimalsV1')
    #self.assertEqual(result.status_code, 301)
    #self.assertEqual(result.headers['location'], 'http://localhost:3033/ebos/AnimalsV1/')

  @patch('githubAPICalls.githubAPICallsClass.getEBOList', return_value=[ 'AnimalsV1', 'BandsV1', 'TownsV1' ])
  @patch('githubAPICalls.githubAPICallsClass.getEBOInfoFileFromGit', return_value='{"Deployments": {"DEV_INT_TEST": "0.0.1"}}')
  @patch('githubAPICalls.githubAPICallsClass.getEBOInfoFileFromGit', return_value='{"Deployments": {"DEV_INT_TEST": "0.0.1"}}')
  @patch('githubAPICalls.githubAPICallsClass.getEBOInfoFileFromGit', return_value='{"Deployments": {"DEV_INT_TEST": "0.0.1"}}')
  @patch('githubAPICalls.githubAPICallsClass.getPythonModelFileFromGit', return_value=model_str)
  @patch('githubAPICalls.githubAPICallsClass.getPythonModelFileFromGit', return_value=model_str)
  @patch('githubAPICalls.githubAPICallsClass.getPythonModelFileFromGit', return_value=model_str)
  def test_animalindexpointsToCorrectSwagger(self, getEBOListCall, getEBOInfoFileFromGit1, getEBOInfoFileFromGit2, getEBOInfoFileFromGit3, getPythonModelFileFromGit1, getPythonModelFileFromGit2, getPythonModelFileFromGit3):
    self.setUpMAN()
    result = self.testClient.get('/ebodocs/AnimalsV1/')
    self.assertEqual(result.status_code, 200, msg='index missing from /ebodocs/AnimalsV1/ not present')
    idx_file = result.get_data(as_text=True)
    print(idx_file)
    self.assertNotEqual(idx_file.find('http://localhost:3033/ebodocs/AnimalsV1/swagger.json'),-1,msg='Could not find correct url for swagger.json in /ebodocs/AnimalsV1/')

