

#Class to represent an endpoint for an EBO
class eboEndpointClass():
  githubAPICalls = None

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

  def __init__(self, eboName, githubAPICalls):
    self.githubAPICalls = githubAPICalls
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
    return self.githubAPICalls.getEBOInfoFileFromMaster(self.eboName)
    
  def firstScanGIT(self):
    try:
      self.state = 'Initial Scanning'
      info = self._getInfo()
      raise Exception('Not Implemented')
    except Exception as e:
      self.setToErrorState(str(e))
      raise #TODO Change back to return
      #return
    self.state = 'OK'

  def updateScanGIT(self):
    try:
      self.state = 'Scanning'
      raise Exception('Not Implemented')
    except Exception as e:
      self.setToErrorState(str(e))
      removeAPI()
      return
    self.state = 'OK'

  def setupAPI(self):
    if self.state != 'OK':
      self._removeAPI()
      return
    raise Exception('Not Implemented')
    
  # may be called if API is not setup
  def _removeAPI(self):
    raise Exception('Not Implemented')


