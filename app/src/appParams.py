from baseapp_for_restapi_backend_with_swagger import readFromEnviroment, getInvalidEnvVarParamaterException
from urllib.parse import urlparse

class appParamsClass():
  APIAPP_ENVIROMENT = None
  APIAPP_GITHUBREPOLOCATION = None
  
  APIAPP_EBOAPIURL = None
  APIAPP_EBOAPIDOCSURL = None

  def __init__(self, env):
    self.APIAPP_ENVIROMENT = readFromEnviroment(env, 'APIAPP_ENVIROMENT', None, None)
    if len(self.APIAPP_ENVIROMENT) < 2:
      raise getInvalidEnvVarParamaterException('APIAPP_ENVIROMENT')
    self.APIAPP_GITHUBREPOLOCATION = readFromEnviroment(env, 'APIAPP_GITHUBREPOLOCATION', None, None)

    self.APIAPP_EBOAPIURL = readFromEnviroment(env, 'APIAPP_EBOAPIURL', None, None)
    self.APIAPP_EBOAPIDOCSURL = readFromEnviroment(env, 'APIAPP_EBOAPIDOCSURL', None, None)


  def printVarValues(self):
    print('APIAPP_ENVIROMENT=' + str(self.APIAPP_ENVIROMENT))
    print('APIAPP_EBOAPIURL=' + str(self.APIAPP_EBOAPIURL))
    print('APIAPP_EBOAPIDOCSURL=' + str(self.APIAPP_EBOAPIDOCSURL))


    
  def getEBOHost(self):
    return urlparse(self.APIAPP_EBOAPIURL).netloc

  def getSanitizedPath(self, url):
    a = urlparse(url).path.strip()
    if (a[-1:] == '/'):
      a = a[:-1]
    return a

  def getEBOPath(self):
    return self.getSanitizedPath(self.APIAPP_EBOAPIURL)

  def overrideEBODOCSPath(self):
    return (self.getEBODOCSPath() != '')

  def getEBODOCSPath(self):
    return self.getSanitizedPath(self.APIAPP_EBOAPIDOCSURL)