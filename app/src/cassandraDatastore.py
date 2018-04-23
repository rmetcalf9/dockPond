import datastore
from cassandra.cluster import Cluster
from baseapp_for_restapi_backend_with_swagger import readFromEnviroment, getInvalidEnvVarParamaterException
import types

#https://datastax.github.io/python-driver/getting_started.html

name = 'Cassandra'

class datastoreClass(datastore.datastoreClass):
  APIAPP_CASS_IPLIST = None
  APIAPP_CASS_PORT = None
  
  cluster = None

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

  def printVarValues(self):
    print('APIAPP_CASS_IPLIST=' + str(self.APIAPP_CASS_IPLIST))
    print('APIAPP_CASS_PORT=' + str(self.APIAPP_CASS_PORT))

  def initStore(self):
    self.cluster = Cluster(self.APIAPP_CASS_IPLIST, port=self.APIAPP_CASS_PORT)


#    CREATE  KEYSPACE [IF NOT EXISTS] keyspace_name 
#   WITH REPLICATION = { 
#      'class' : 'SimpleStrategy', 'replication_factor' : N } 
#     | 'class' : 'NetworkTopologyStrategy', 
#       'dc1_name' : N [, ...] 
#   }
