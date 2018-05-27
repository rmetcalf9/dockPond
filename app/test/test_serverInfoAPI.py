from TestHelperSuperClass import testHelperAPIClient, env
import unittest
import json
from unittest.mock import patch, call
from appObj import getAppObj

data_simpleJobCreateParams = {
  "name": "TestJob",
  "repetitionInterval": "HOURLY:03",
  "command": "ls",
  "enabled": True
}

class test_api(testHelperAPIClient):

  @patch('githubAPICalls.githubAPICallsClass.getEBOList', return_value=[ 'AnimalsV1', 'BandsV1', 'TownsV1' ])
  def test_getServerInfo(self, getEBOListCall):
    self.setUpMAN()
    expRes = {
      'Instance': {
        'APIAPP_EBOAPIDOCSURL': 'http://localhost:3033/ebodocs',
        'APIAPP_EBOAPIURL': 'http://localhost:3033/ebos',
        'APIAPP_ENVIROMENT': 'DEV_INT_TEST',
        "APIAPP_GITHUBREPOLOCATION": 'https://github.com/rmetcalf9/dockPondSampleEBOs'
      },
      'EBOs': {
        'NumberLoaded': 3,
        'NumberNotOK': 0
      }
    }
    result = self.testClient.get('/api/serverinfo/')
    self.assertEqual(result.status_code, 200)
    resultJSON = json.loads(result.get_data(as_text=True))
    self.assertJSONStringsEqual(resultJSON, expRes)
    


  @patch('githubAPICalls.githubAPICallsClass.getEBOList', return_value=[ 'AnimalsV1', 'BandsV1', 'TownsV1' ])
  def test_devModeOptionsCorrectHeaderResponse(self, getEBOListCall):
    
    alteredEnv = dict(env)
    alteredEnv['APIAPP_MODE']='DEVELOPER'
    
    getAppObj().init(alteredEnv, watcherThread = None, testingMode = True)
    self.testClient = getAppObj().flaskAppObject.test_client()
    self.testClient.testing = True 
    result = self.testClient.options('/api/serverinfo/')
    foundHeaders = dict()
    for header in result.headers:
      self.assertFalse(header[0] in foundHeaders,msg='Found duplicate header in options response - ' + header[0])
      foundHeaders[header[0]] = header[1]

