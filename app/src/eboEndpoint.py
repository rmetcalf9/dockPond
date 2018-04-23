

#Class to represent an endpoint for an EBO
class eboEndpointClass():
  state = 'Uninstalised'
  stateMeanings = {
    'Uninstalised': 'Not instalised',
    'Ready to Scan': 'Instalised',
    'Scanning': 'Querying git to get model',
    'OK': 'Model loaded and API active',
    'Error': 'Loaded from GIT but API inactive due to an error',
    'Vanished': 'In memory but last scan of git showed this EBO has dissapeared',
    'Invalid Name': 'EBO name read from git dosen\'t conform to required standard'
  }
  eboName = None
  errorStateReason = None

  def __init__(self, eboName):
    self.state = 'Uninstalised'
    self.eboName = eboName
    if not self.isValidName:
      self.state = 'Invalid Name'
      self.errorStateReason = 'Invalid Name'
      return
    self.state = 'Ready to Scan'

  #Make sure name read from git is a valid name for an EBO
  def isValidName(self):
    #TODO
    return True

  def setToErrorState(self, reasonMessage):
    self.state = 'Error'
    self.errorStateReason = reasonMessage
    
  def markVanished(self):
    self.state = 'Vanished'
    self.errorStateReason = 'Not found in latest git scan'

  def scanGIT(self):
    raise Exception('Not Implemented')

  def setupAPI(self):
    raise Exception('Not Implemented')
    
  # may be called if API is not setup
  def removeAPI(self):
    raise Exception('Not Implemented')

  #Called for an initial scan and for a refresh.
  def scanGITandRegisterAPI(self):
    self.state = 'Scanning'
    try:
      scanGIT()
      setupAPI()
    except Exception as e:
      self.setToErrorState(str(e))
      removeAPI()
      return
    self.state='OK'
