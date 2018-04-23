from baseapp_for_restapi_backend_with_swagger import readFromEnviroment, getInvalidEnvVarParamaterException

class appParamsClass():
  APIAPP_ENVIROMENT = None
  APIAPP_GITHUBREPOLOCATION = None

  def __init__(self, env):
    self.APIAPP_ENVIROMENT = readFromEnviroment(env, 'APIAPP_ENVIROMENT', None, None)
    if len(self.APIAPP_ENVIROMENT) < 2:
      raise getInvalidEnvVarParamaterException('APIAPP_ENVIROMENT')
    self.APIAPP_GITHUBREPOLOCATION = readFromEnviroment(env, 'APIAPP_GITHUBREPOLOCATION', None, None)


  def printVarValues(self):
    print('APIAPP_ENVIROMENT=' + str(self.APIAPP_ENVIROMENT))

