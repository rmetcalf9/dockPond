import json

#Required for get Model execution
from flask_restplus import fields

from apiEndpoint import apiEndpointClass

def getGetModelFunctionFromPythonFile(pythonFile):
  ldict = locals()
  exec(pythonFile, None,ldict)
  return ldict['getModel']

def getEBOModel(appObj):
  # used to describe GET /EBOs query result record
  return appObj.flastRestPlusAPIObject.model('EBO', {
    'name': fields.String(default='',description='Name of this EBO'),
    'state': fields.String(default='',description='State'),
    'stateMeaning': fields.String(default='',description='Text description of state meaning'),
    'sourceFileTag': fields.String(default='',description='Github tag for source file of the EBO'),
    'loadedAPITag': fields.String(default='',description='Github tag for loaded API'),
    'errorStateReason': fields.String(default='',description='Error details for any error encountered when setting up the API for this EBO'),
    'apiurl': fields.String(default='',description='URL for api'),
    'apidocurl': fields.String(default='',description='URL for api documentation'),
    'swaggerurl': fields.String(default='',description='URL for swagger.json file')
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
  
  pythonFile = None
  pythonFileTag = None
  loadedAPI = None
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
    ret['state'] = self.state
    ret['stateMeaning'] = self.stateMeanings[self.state]
    ret['loadedAPITag'] = self.loadedAPITag
    ret['sourceFileTag'] = self.pythonFileTag
    ret['errorStateReason'] = self.errorStateReason
    ret['apiurl'] = self.appObj.appParams.APIAPP_EBOAPIURL + '/' + self.eboName + '/EBO/'
    ret['apidocurl'] = self.appObj.appParams.APIAPP_EBOAPIDOCSURL + '/' + self.eboName + '/'
    ret['swaggerurl'] = self.appObj.appParams.APIAPP_EBOAPIURL + '/' + self.eboName + '/swagger.json' #Give out API location

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
  def _loadModelFN(self, tagName):
    pythonFile = self.githubAPICalls.getPythonModelFileFromGit(self.eboName, tagName)
    
    #Last statements so not run if execption has occured
    self.pythonFile = pythonFile
    self.pythonFileTag = tagName
  
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
      if self.pythonFileTag != tagGitSaysWeShouldBeRunning:
        self._loadModelFN(tagGitSaysWeShouldBeRunning)
        if self.pythonFileTag == tagGitSaysWeShouldBeRunning:
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
    self._scanGIT(noDepState='Not deployed in this Instance', finishLoadState='Require Model Update')

  def _setupAPI(self):
    try:
      if self.loadedAPI is not None:
        self.loadedAPI.unload()
        self.loadedAPI = None
        self.loadedAPITag = None
      self.loadedAPI = apiEndpointClass(self)
      self.loadedAPITag = self.pythonFileTag
    except Exception as e:
      self.setToErrorState(str(e))
      raise #Used to display errors
      ##return
    self.state = 'OK'
  
  def setupAPI(self):
    if self.state == 'Require Model Update':
      self.state = 'Model Update'
      self._setupAPI()
    if self.state == 'Require Model Load':
      self.state = 'Model Load'
      self._setupAPI()
    return
    


