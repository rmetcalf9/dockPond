from TestHelperSuperClass import testHelperAPIClient
import unittest
import json
from unittest.mock import patch, call

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
      'EBOs': {
        'NumberLoaded': 3,
        'NumberNotOK': 0
      }
    }
    result = self.testClient.get('/api/serverinfo/')
    self.assertEqual(result.status_code, 200)
    resultJSON = json.loads(result.get_data(as_text=True))
    self.assertJSONStringsEqual(resultJSON, expRes)




