import json

#Required for get Model execution
from flask_restplus import fields

def getGetModelFunctionFromPythonFile(pythonFile):
  ldict = locals()
  exec(pythonFile, None,ldict)
  return ldict['getModel']

def getEBOModel(appObj):
  # used to describe GET /EBOs query result record
  return appObj.flastRestPlusAPIObject.model('EBO', {
    'name': fields.String(default='',description='Name of this EBO')
  })

  
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
    'Require Model Update': 'Loaded API and latest scanned model are different versions.',
    'Require Model Load': 'New EBO found - API needs to be setup',
    'Model Update': 'Updating the API Model',
    'Model Load': 'Loading the API Model',
    'OK': 'Model loaded and API active',
    'Error': 'Loaded from GIT but API inactive due to an error',
    'Vanished': 'In memory but last scan of git showed this EBO has dissapeared',
    'Invalid Name': 'EBO name read from git dosen\'t conform to required standard',
    'Not deployed in this Instance': 'EBOs info file dosen\'t indicate it should be deployed in this instance. These are filtered out of reports.'
  }
  eboName = None
  errorStateReason = None
  
  loadedModel = None
  loadedModelTag = None
  loadedAPITag = None

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

  def getDictForQueryMustMatchModel(self):
    ret = dict()
    ret['name'] = self.eboName
    return ret
    
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
    return json.loads(self.githubAPICalls.getEBOInfoFileFromGit(self.eboName, 'master'))
  
  # Called by scanGIT - dosen't need to change state
  def _loadModel(self, tagName):
    pythonFile = self.githubAPICalls.getPythonModelFileFromGit(self.eboName, tagName)
    getModel = getGetModelFunctionFromPythonFile(pythonFile)
    if getModel is None:
      raise Exception('Failed to load model - (getModel = None)')
    model = getModel(self.appObj)
    
    #Last statements so not run if execption has occured
    self.loadedModel = model
    self.loadedModelTag = tagName
  
  def _scanGIT(self, noDepState, finishLoadState):
    try:
      self.state = 'Initial Scanning'
      info = self._getInfo()
      tagGitSaysWeShouldBeRunning = None
      for depEnv in info['Deployments']:
        if depEnv == self.appObj.appParams.APIAPP_ENVIROMENT:
          tagGitSaysWeShouldBeRunning = info['Deployments'][depEnv]
      if tagGitSaysWeShouldBeRunning is None:
        self.state = noDepState
        return
      if self.loadedModelTag != tagGitSaysWeShouldBeRunning:
        self._loadModel(tagGitSaysWeShouldBeRunning)
        if self.loadedModelTag == tagGitSaysWeShouldBeRunning:
          self.state = finishLoadState
        return
    except Exception as e:
      self.setToErrorState(str(e))
      ##raise #Used to display errors
      return
    self.state = 'OK'
  
  def firstScanGIT(self):
    self._scanGIT(noDepState='Not deployed in this Instance', finishLoadState='Require Model Load')

  def updateScanGIT(self):
    self._scanGIT(noDepState='Vanished', finishLoadState='Require Model Update')

  def _setupAPI(self):
    try:
      raise Exception('_setupAPI Not Implemented')
    except Exception as e:
      self.setToErrorState(str(e))
      ##raise #Used to display errors
      return
    self.state = 'OK'
  
  def setupAPI(self):
    if self.state == 'Require Model Update':
      self.state = 'Model Update'
      self._setupAPI()
    if self.state == 'Require Model Load':
      self.state = 'Model Load'
      self._setupAPI()
    return
    


