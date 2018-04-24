#tests for appObj
from TestHelperSuperClass import testHelperAPIClient
from appObj import appObj, appObjClass
import pytz
import datetime
import json
from unittest.mock import patch, call

class test_appObjClass(testHelperAPIClient):
#Actual tests below

  
  @patch('githubAPICalls.githubAPICallsClass.getEBOList', return_value=[ 'AnimalsV1', 'BandsV1', 'TownsV1' ])
  def test_CreateAppOBjInstance(self, getEBOListCall):
    self.setUpMAN()


