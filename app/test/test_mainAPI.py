from TestHelperSuperClass import testHelperAPIClient
import unittest
import json
from unittest.mock import patch, call

class test_mainAPI(testHelperAPIClient):

  @patch('githubAPICalls.githubAPICallsClass.getEBOList', return_value=[ 'AnimalsV1', 'BandsV1', 'TownsV1' ])
  def test_getEBOs(self, getEBOListCall):
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
    for expIdx, expVal in enumerate(resultJSON['result']):
      for idx, val in enumerate(matchedARR):
        if self.areJSONStringsEqual(val,expVal):
          matchedARR[idx] = '_'
          numMatched = numMatched + 1
    self.assertEqual(len(matchedARR),numMatched,msg='Didn\'t match all results')

  @patch('githubAPICalls.githubAPICallsClass.getEBOList', return_value=[ 'AnimalsV1', 'BandsV1', 'TownsV1' ])
  def test_swaggerJSONProperlyShared(self, getEBOListCall):
    self.setUpMAN()
    result = self.testClient.get('/api/swagger.json')
    self.assertEqual(result.status_code, 200)
    result = self.testClient.get('/apidocs/swagger.json')
    self.assertEqual(result.status_code, 200)



