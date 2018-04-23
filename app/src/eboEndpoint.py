

#Class to represent an endpoint for an EBO
class eboEndpointClass():
  githubAPICalls = None
  appObj = None

  state = 'Uninstalised'
  stateMeanings = {
    'Uninstalised': 'Not instalised',
    'Ready to Scan': 'Instalised',
    'Initial Scanning': 'Querying git to get model (First time EBO has been seen)',
    'Scanning': 'Querying git to get model',
    'OK': 'Model loaded and API active',
    'Error': 'Loaded from GIT but API inactive due to an error',
    'Vanished': 'In memory but last scan of git showed this EBO has dissapeared',
    'Invalid Name': 'EBO name read from git dosen\'t conform to required standard',
    'Not deployed in this Instance': 'EBOs info file dosen\'t indicate it should be deployed in this instance. These are filtered out of reports.'
  }
  eboName = None
  errorStateReason = None

  def __init__(self, eboName, githubAPICalls, appObj):
    self.githubAPICalls = githubAPICalls
    self.appObj = appObj
    self.state = 'Uninstalised'
    self.eboName = eboName
    if not self._isValidName:
      self.state = 'Invalid Name'
      self.errorStateReason = 'Invalid Name'
      return
    self.state = 'Ready to Scan'

  #Make sure name read from git is a valid name for an EBO
  def _isValidName(self):
    #TODO
    return True

  def setToErrorState(self, reasonMessage):
    self.state = 'Error'
    self.errorStateReason = reasonMessage
    
  def markVanished(self):
    self.state = 'Vanished'
    self.errorStateReason = 'Not found in latest git scan'

  def _getInfo(self):
    return self.githubAPICalls.getEBOInfoFileFromGit(self.eboName, 'master')
  
  def _scanGIT(self, noDepState):
    try:
      self.state = 'Initial Scanning'
      info = self._getInfo()
      tagForDeployment = None
      for depEnv in info['Deployments']:
        if depEnv == self.appObj.appParams.APIAPP_ENVIROMENT:
          tagForDeployment = info['Deployments'][depEnv]
      if tagForDeployment is None:
        self.state = noDepState
        return
      raise Exception('Not Implemented Deploy tag ' + tagForDeployment)
    except Exception as e:
      self.setToErrorState(str(e))
      raise #TODO Change back to return
      #return
    self.state = 'OK'
  
  def firstScanGIT(self):
    self._scanGIT(noDepState='Not deployed in this Instance')

  def updateScanGIT(self):
    self._scanGIT(noDepState='Vanished')

  def setupAPI(self):
    if self.state != 'OK':
      #self._removeAPI() We will never remove an API that is present
      return
    raise Exception('Not Implemented')
    


