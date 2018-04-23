# datastore contains datastoreClass
# this is the base object used for datastores. Initially I will implement cassandra
# but this abstraction will allow me to add other abstractions later
# the functions here are designed to be overridden

class datastoreClass():
  typeName = 'NotDefined' #type name for datastore e.g. cassendra, etc
  datastoreNotOveriddenException = Exception("Function not implemented for this datastre type")
  enviromentName = 'NULL' #String representing the enviroment name e.g. Dev, Test, Prod.

  # Should evaluate paramaters but not do any db connections
  def __init__(self,typeName, enviromentName):
    self.typeName = typeName
    self.datastoreNotOveriddenException =  Exception("Function not implemented for " + self.typeName + " type")
    self.enviromentName = enviromentName

  # Called when starting to output values
  def printVarValues(self):
    raise self.datastoreNotOveriddenException

  #called when the application is initially started
  # all inits may be called when the store is already instalised
  def initStore(self):
    raise self.datastoreNotOveriddenException

  #Called once to init each object type
  # this is called when duckPond recognises the need for the type
  # may be called mutiple times
  def initObjectType(self, objectTypeName):
    raise self.datastoreNotOveriddenException

  #function to create new instance of obj or update it's data
  # objData is a DICT that is converted to JSON string for storing in DB
  def upsert(self, objectTypeName, objKey, objData):
    raise self.datastoreNotOveriddenException

  def delete(self, objectTypeName, objKey):
    raise self.datastoreNotOveriddenException

  #function to take the objKey and return the data
  def query(self, objectTypeName, objKey):
    raise self.datastoreNotOveriddenException

  #Granular updates not required by dockPond so not implemented

  #Complex queries not implemented in dockPond other ways to access the datastore should be used

