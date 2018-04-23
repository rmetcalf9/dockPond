from TestHelperSuperClass import testHelperSuperClass
from githubAPICalls import githubAPICallsClass

class mockAppParamsClass():
  APIAPP_GITHUBREPOLOCATION = 'https://api.github.com/repos/rmetcalf9/dockPondSampleEBOs'

class mockAppObjClass():
  appParams = mockAppParamsClass()

class test_appCassandraDatastoreClass(testHelperSuperClass):

  def testListEBOs(self):
    pass #removed due to API call limit
    #api = githubAPICallsClass(mockAppObjClass)
    #EBOList = api.getEBOList()
    #if not 'Animals' in EBOList:
    #  self.assertFalse(True, msg='Could not find EBO Animals in github repo')
