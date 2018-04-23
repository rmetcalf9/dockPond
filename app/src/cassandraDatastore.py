import datastore
from cassandra.cluster import Cluster
from baseapp_for_restapi_backend_with_swagger import readFromEnviroment, getInvalidEnvVarParamaterException
import types
import json

#https://datastax.github.io/python-driver/getting_started.html


name = 'Cassandra'

class datastoreClass(datastore.datastoreClass):
  keyspace_prefix = 'DP_'

  APIAPP_CASS_IPLIST = None
  APIAPP_CASS_PORT = None
  APIAPP_CASS_REPLICATION = None
  
  cluster = None
  
  def keyspace(self):
    return self.keyspace_prefix + self.enviromentName

  # Fed in the enviroment to enable it to read CAS params
  def __init__(self,enviromentName, env):
    super().__init__('Cassandra', enviromentName)
    APIAPP_CASS_IPLISTSTR = readFromEnviroment(env, 'APIAPP_CASS_IPLIST', None, None, nullValueAllowed=True)
    try:
      self.APIAPP_CASS_IPLIST = eval(APIAPP_CASS_IPLISTSTR)
    except:
      raise getInvalidEnvVarParamaterException('APIAPP_CASS_IPLIST', actualValue=APIAPP_CASS_IPLISTSTR, messageOverride=None)
    if not isinstance(self.APIAPP_CASS_IPLIST, list):
      print('Error not a list')
      raise getInvalidEnvVarParamaterException('APIAPP_CASS_IPLIST', actualValue=APIAPP_CASS_IPLISTSTR, messageOverride='Not a list')
    if len(self.APIAPP_CASS_IPLIST) == 0:
      print('Empty list')
      raise getInvalidEnvVarParamaterException('APIAPP_CASS_IPLIST', actualValue=APIAPP_CASS_IPLISTSTR, messageOverride='Empty list')
    for curEndPoint in self.APIAPP_CASS_IPLIST:
      if not isinstance(curEndPoint, str):
        print('Endpoint passed is not a string')
        raise getInvalidEnvVarParamaterException('APIAPP_CASS_IPLIST', actualValue=APIAPP_CASS_IPLISTSTR, messageOverride='One item is not a string')
    
    APIAPP_CASS_PORTSTR = readFromEnviroment(env, 'APIAPP_CASS_PORT', None, None, nullValueAllowed=False)
    try:
      self.APIAPP_CASS_PORT = int(APIAPP_CASS_PORTSTR)
    except:
      raise getInvalidEnvVarParamaterException('APIAPP_CASS_PORT', actualValue=APIAPP_CASS_PORTSTR, messageOverride='Port must be a number')

    APIAPP_CASS_REPLICATIONSTR = readFromEnviroment(env, 'APIAPP_CASS_REPLICATION', None, None, nullValueAllowed=False)
    # Looks like JSON but isn't because values have ' not "
    #try:
    #  self.APIAPP_CASS_REPLICATION = json.loads(APIAPP_CASS_REPLICATIONSTR)
    #except:
    #  raise getInvalidEnvVarParamaterException('APIAPP_CASS_REPLICATION', actualValue=APIAPP_CASS_REPLICATIONSTR, messageOverride='Invalid JSON')
    self.APIAPP_CASS_REPLICATION = APIAPP_CASS_REPLICATIONSTR

  def printVarValues(self):
    print('APIAPP_CASS_IPLIST=' + str(self.APIAPP_CASS_IPLIST))
    print('APIAPP_CASS_PORT=' + str(self.APIAPP_CASS_PORT))

  def initStore(self):
    self.cluster = Cluster(self.APIAPP_CASS_IPLIST, port=self.APIAPP_CASS_PORT)
    session = self.cluster.connect()
    cql = 'CREATE KEYSPACE IF NOT EXISTS ' + self.keyspace() + ' WITH REPLICATION = ' + self.APIAPP_CASS_REPLICATION
    # print(cql)
    session.execute(cql)
    session.shutdown()

  def initObjectType(self, objectTypeName):
    #session = self.cluster.connect(self.keyspace())
    
    session = self.cluster.connect()
    cql = 'CREATE TABLE IF NOT EXISTS ' + self.keyspace() + '.' + objectTypeName + ' ( id text, jsonstr text, PRIMARY KEY (id) )'
    # print(cql)
    session.execute(cql)
    session.shutdown()

  def upsert(self, objectTypeName, objKey, objData):
    session = self.cluster.connect()
    cql = 'INSERT INTO ' + self.keyspace() + '.' + objectTypeName + ' (id, jsonstr) VALUES ( %s, %s)'
    # print(cql)
    session.execute(cql, (objKey, json.dumps(objData)))
    session.shutdown()

  def query(self, objectTypeName, objKey):
    session = self.cluster.connect()
    cql = 'select * from ' + self.keyspace() + '.' + objectTypeName + ' WHERE ID=\'' + objKey + '\''
    rows = session.execute(cql)
    if rows.has_more_pages:
      raise Exception('More than one page of objects with this key returned')
    c = 0
    for curRow in rows:
      c = c + 1
    if c > 1:
      raise Exception('More than one object with this key returned')
    return json.loads(curRow.jsonstr)

  def delete(self, objectTypeName, objKey):
    raise Exception('TODO')

