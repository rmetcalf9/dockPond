from baseapp_for_restapi_backend_with_swagger import readFromEnviroment, getInvalidEnvVarParamaterException

class appParamsClass():
  APIAPP_ENVIROMENT = None


  APIAPP_CASS_IPLIST = None
  APIAPP_CASS_PORT = None


  def __init__(self, env):
    self.APIAPP_ENVIROMENT = readFromEnviroment(env, 'APIAPP_ENVIROMENT', None, None)
    if len(self.APIAPP_ENVIROMENT) < 2:
      raise getInvalidEnvVarParamaterException('APIAPP_ENVIROMENT')

    self.APIAPP_CASS_IPLISTSTR = readFromEnviroment(env, 'APIAPP_CASS_IPLIST', None, None)
    self.APIAPP_CASS_IPLIST = []
    raise Exception('TODO')


    self.APIAPP_CASS_PORT = readFromEnviroment(env, 'APIAPP_CASS_PORT', None, None)

