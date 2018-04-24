#tests for appObj
from TestHelperSuperClass import testHelperSuperClass
from cassandraDatastore import datastoreClass as cassandraDatastoreClass
import pytz
import datetime
import json
from baseapp_for_restapi_backend_with_swagger import getInvalidEnvVarParamaterException
from cassandra.cluster import Cluster

# These tests test against a local deployed cassandra instance

workingenv = {
  'APIAPP_CASS_PORT': '9042',
  'APIAPP_CASS_IPLIST': '[ "localhost"]',
  'APIAPP_CASS_REPLICATION': "{ 'class': 'SimpleStrategy', 'replication_factor': '1' }"
}

class test_appCassandraDatastoreClass(testHelperSuperClass):


#Actual tests below

  def test_initCreateObj(self):
    dataStore = cassandraDatastoreClass('DEVTST_UNT',workingenv)
    dataStore.initStore()
    dataStore.initObjectType("AnimalsV1")

    #Check table was created
    cluster = Cluster(eval(workingenv['APIAPP_CASS_IPLIST']), port=int(workingenv['APIAPP_CASS_PORT']))
    session = cluster.connect()
    cql = 'USE ' + dataStore.keyspace()
    session.execute(cql)
    cql = 'select * from AnimalsV1 WHERE ID=\'ABC\''
    res = session.execute(cql)
    session.shutdown()

  def test_initAddSingleItemObj(self):
    tstType = "Animals2"
    tstDataID = 'ABC'
    tstData = { 'ID': tstDataID, 'Name': 'Don\'t know' }

    dataStore = cassandraDatastoreClass('DEVTST_UNT',workingenv)
    dataStore.initStore()
    dataStore.initObjectType(tstType)
    dataStore.upsert(tstType, tstDataID, tstData)

    #Check table was created
    cluster = Cluster(eval(workingenv['APIAPP_CASS_IPLIST']), port=int(workingenv['APIAPP_CASS_PORT']))
    session = cluster.connect()
    cql = 'USE ' + dataStore.keyspace()
    session.execute(cql)
    cql = 'select * from ' + tstType + ' WHERE ID=\'' + tstDataID + '\''
    rows = session.execute(cql)
    self.assertFalse(rows.has_more_pages)
    c = 0
    for curRow in rows:
      c = c + 1
    self.assertEqual(c,1,msg="Query didn't return single object")
    self.assertEqual(curRow.id,tstDataID)
    self.assertJSONStringsEqual(json.loads(curRow.jsonstr),tstData,msg='Different Data Returned')
    session.shutdown()

  def test_initQueryBackSingleItemObj(self):
    tstType = "Animals3"
    tstDataID = 'ABC'
    tstData = { 'ID': tstDataID, 'Name': 'Don\'t know' }

    dataStore = cassandraDatastoreClass('DEVTST_UNT',workingenv)
    dataStore.initStore()
    dataStore.initObjectType(tstType)
    dataStore.upsert(tstType, tstDataID, tstData)
    dataVal = dataStore.query(tstType, tstDataID)
    self.assertJSONStringsEqual(dataVal,tstData,msg='Different Data Returned')

  def test_DeleteSingleItemObj(self):
    tstType = "Animals4"
    tstDataID = 'ABC'
    tstData = { 'ID': tstDataID, 'Name': 'Don\'t know' }

    dataStore = cassandraDatastoreClass('DEVTST_UNT',workingenv)
    dataStore.initStore()
    dataStore.initObjectType(tstType)
    dataStore.upsert(tstType, tstDataID, tstData)
    dataVal = dataStore.query(tstType, tstDataID)
    self.assertJSONStringsEqual(dataVal,tstData,msg='Different Data Returned')
    deletedVal = dataStore.delete(tstType, tstDataID)
    self.assertJSONStringsEqual(deletedVal,tstData,msg='Different Data Returned from delete function')
    with self.assertRaises(Exception) as context:
      dataVal = dataStore.query(tstType, tstDataID)
    self.checkGotRightException(context,dataStore.objectNotFoundException)


