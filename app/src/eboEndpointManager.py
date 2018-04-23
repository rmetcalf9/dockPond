from eboEndpoint import eboEndpointClass
from githubAPICalls import githubAPICallsClass

#Class to represent loaded EBOs
class eboEndpointManagerClass():
  githubAPICalls = None

  loadedEBOs = None #Dict of eboEndpoint objects
  
  def __init__(self, appObj):
    self.loadedEBOs = dict()
    self.githubAPICalls = githubAPICallsClass(appObj)


  def scanGitandLoadEBOs(self):
    gitEBOs = self.githubAPICalls.getEBOList()
    
    #Mark vanished
    for loadedEBO in self.loadedEBOs:
      if not loadedEBO.eboName in gitEBOs:
        loadedEBO.markVanished()
    
    for gitEBO in gitEBOs:
      if gitEBO in self.loadedEBOs:
        self.loadedEBOs[gitEBO].scanGITandRegisterAPI()
      else:
        newEBO = eboEndpointClass(gitEBO)
        newEBO.scanGITandRegisterAPI()
        self.loadedEBOs.append(gitEBO)


