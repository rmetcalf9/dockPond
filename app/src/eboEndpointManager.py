from eboEndpoint import eboEndpointClass
from githubAPICalls import githubAPICallsClass

#Class to represent loaded EBOs
class eboEndpointManagerClass():
  appObj = None
  githubAPICalls = None

  loadedEBOs = None #Dict of eboEndpoint objects
  
  def __init__(self, appObj):
    self.loadedEBOs = dict()
    self.appObj = appObj
    self.githubAPICalls = githubAPICallsClass(appObj)


  def scanGitandLoadEBOs(self):
    print("Querying github for EBO List...", end='')
    gitEBOs = self.githubAPICalls.getEBOList()
    print("Found " + str(len(gitEBOs)) + " EBOs")
    
    #Mark vanished
    for loadedEBO in self.loadedEBOs:
      if not loadedEBO.eboName in gitEBOs:
        loadedEBO.markVanished()
    
    for gitEBO in gitEBOs:
      if gitEBO in self.loadedEBOs:
        self.loadedEBOs[gitEBO].updateScanGIT()
        self.loadedEBOs[gitEBO].setupAPI() #Will remove API if EBO is not in OK state
      else:
        newEBO = eboEndpointClass(gitEBO, self.githubAPICalls, self.appObj)
        newEBO.firstScanGIT()
        newEBO.setupAPI()
        self.loadedEBOs[newEBO.eboName] = newEBO #appended to list whatever state is


