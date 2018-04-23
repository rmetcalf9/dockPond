#tests for appObj
from TestHelperSuperClass import testHelperSuperClass
from cassandraDatastore import datastoreClass as cassandraDatastoreClass
import pytz
import datetime
import json
from baseapp_for_restapi_backend_with_swagger import getInvalidEnvVarParamaterException

workingenv = {
  'APIAPP_CASS_PORT': '9000',
  'APIAPP_CASS_IPLIST': '[ "1.2.3.4", "4.3.2.1"]'
}

class test_appCassandraDatastoreClass(testHelperSuperClass):
#Actual tests below

  def test_InvalidPortInstance(self):
    invalidenv = dict(workingenv)
    invalidenv['APIAPP_CASS_PORT'] = 'NOTANUM344'
    with self.assertRaises(Exception) as context:
      x = cassandraDatastoreClass('DEV',invalidenv)
    self.checkGotRightException(context,getInvalidEnvVarParamaterException('APIAPP_CASS_PORT'))


  def test_InvalidIPListInstance(self):
    invalidenv = dict(workingenv)
    invalidenv['APIAPP_CASS_IPLIST'] = 'NOTANUM344VALIDLIST'
    with self.assertRaises(Exception) as context:
      x = cassandraDatastoreClass('DEV',invalidenv)
    self.checkGotRightException(context,getInvalidEnvVarParamaterException('APIAPP_CASS_IPLIST'))

  def test_InvalidIPListInstanceBadContent(self):
    invalidenv = dict(workingenv)
    invalidenv['APIAPP_CASS_IPLIST'] = '[ "1.2.3.4", "fdfdsf.fdsd.fdsfds.fdsfds", None ]'
    with self.assertRaises(Exception) as context:
      x = cassandraDatastoreClass('DEV',invalidenv)
    self.checkGotRightException(context,getInvalidEnvVarParamaterException('APIAPP_CASS_IPLIST'))


