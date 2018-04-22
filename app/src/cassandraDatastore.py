import datastore
from cassandra.cluster import Cluster

#https://datastax.github.io/python-driver/getting_started.html

class cassandraDatastoreClass(datastore.datastoreClass):

  def __init__(self,enviromentName, clusterIPList, port):
    super().__init__('Cassandra', enviromentName)
    cluster = Cluster(clusterIPList, port=port)


#    CREATE  KEYSPACE [IF NOT EXISTS] keyspace_name 
#   WITH REPLICATION = { 
#      'class' : 'SimpleStrategy', 'replication_factor' : N } 
#     | 'class' : 'NetworkTopologyStrategy', 
#       'dc1_name' : N [, ...] 
#   }
