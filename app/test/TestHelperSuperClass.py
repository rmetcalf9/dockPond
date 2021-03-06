#Test helper functions
# defines a baseclass with extra functions
# https://docs.python.org/3/library/unittest.html
import unittest
import json
from appObj import getAppObj

import datetime
import pytz
from baseapp_for_restapi_backend_with_swagger import from_iso8601


env = {
  'APIAPP_PORT': '3033',
  'APIAPP_MODE': 'DOCKER',
  'APIAPP_VERSION': 'TEST-3.3.3',
  'APIAPP_FRONTEND': '../app',
  'APIAPP_APIURL': 'http://localhost:3033/api',
  'APIAPP_APIDOCSURL': 'http://localhost:3033/apidocs',
  'APIAPP_APIACCESSSECURITY': '[{ "type": "basic-auth" }]',
  'APIAPP_EBOAPIURL': 'http://localhost:3033/ebos',
  'APIAPP_EBOAPIDOCSURL': 'http://localhost:3033/ebodocs',
  'APIAPP_ENVIROMENT': 'DEV_INT_TEST',
  'APIAPP_CASS_PORT': '9042',
  'APIAPP_CASS_IPLIST': '[ "localhost"]',
  'APIAPP_CASS_REPLICATION': '{ \'class\': \'SimpleStrategy\', \'replication_factor\': \'1\' }',
  'APIAPP_GITHUBREPOLOCATION': 'https://api.github.com/repos/rmetcalf9/dockPondSampleEBOs'
}
#If 403s get returned check
# https://api.github.com/repos/rmetcalf9/dockPondSampleEBOs/rate_limit
# https://api.github.com/rate_limit

class testHelperSuperClass(unittest.TestCase):
  def checkGotRightException(self, context, ExpectedException):
    if (context.exception != None):
      if (context.exception != ExpectedException):
        print("**** Wrong exception raised:")
        print("      expected: " + type(ExpectedException).__name__ + ' - ' + str(ExpectedException));
        print("           got: " + type(context.exception).__name__ + ' - ' + str(context.exception));
        raise context.exception
    self.assertTrue(ExpectedException == context.exception)

  def areJSONStringsEqual(self, str1, str2):
    a = json.dumps(str1, sort_keys=True)
    b = json.dumps(str2, sort_keys=True)
    return (a == b)

  def assertJSONStringsEqual(self, str1, str2, msg=''):
    if (self.areJSONStringsEqual(str1,str2)):
      return
    print("Mismatch JSON")
    a = json.dumps(str1, sort_keys=True)
    b = json.dumps(str2, sort_keys=True)
    print(a)
    print("--")
    print(b)
    self.assertTrue(False, msg=msg)

  def assertTimeCloseToCurrent(self, time, msg='Creation time is more than 3 seconds adrift'):
    if (isinstance(time, str)):
      time = from_iso8601(time)
    curTime = datetime.datetime.now(pytz.timezone("UTC"))
    time_diff = (curTime - time).total_seconds()
    self.assertTrue(time_diff < 3, msg=msg)
    
#helper class with setup for an APIClient
class testHelperAPIClient(testHelperSuperClass):
  testClient = None

  def setUp(self):
    pass

  #moved to a manual call so I can inject and stop call to hithub api
  def setUpMAN(self):
    getAppObj().init(env, watcherThread = None, testingMode = True)
    self.testClient = getAppObj().flaskAppObject.test_client()
    self.testClient.testing = True 
  def tearDown(self):
    self.testClient = None



