from TestHelperSuperClass import testHelperAPIClient
from unittest.mock import patch, call
import eboEndpointManager
import json
from appObj import getAppObj


class test_eboEndpointManager(testHelperAPIClient):

  @patch('githubAPICalls.githubAPICallsClass.getEBOList', return_value=[ 'AnimalsV1' ])
  @patch('githubAPICalls.githubAPICallsClass.getEBOInfoFileFromGit', return_value='{"Deployments": {"NOT_DEV_INT_TEST": "0.0.1"}}')
  def test_scanAndLoadEBONotDeployedTwice(self, getEBOListCall, getEBOInfoFileFromGit):
    self.setUpMAN()
    result = self.testClient.get('/api/EBOs/')
    self.assertEqual(result.status_code, 200)
    resultJSON = json.loads(result.get_data(as_text=True))
    self.assertEqual(resultJSON['result'][0]['state'],'Not deployed in this Instance', msg='EBO is in wrong state')
    getAppObj().eboEndpointManager.scanGitandLoadEBOs()
    result2 = self.testClient.get('/api/EBOs/')
    self.assertEqual(result2.status_code, 200)
    result2JSON = json.loads(result2.get_data(as_text=True))
    self.assertEqual(result2JSON['result'][0]['state'],'Not deployed in this Instance', msg='EBO is in wrong state')



