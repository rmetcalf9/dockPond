import requests
import json
import urllib


class githubAPICallsClass():
  apiURL = None

  def __init__(self, appObj):
    self.apiURL = appObj.appParams.APIAPP_GITHUBREPOLOCATION
    
  def c_get(self,api,expected_responses):
    r = requests.get(self.apiURL + api)
    if r.status_code in expected_responses:
      return r
    raise Exception('Unexpected response from get:' + api + ' (' + str(r.status_code) + ')')
  def c_delete(self,api,expected_responses):
    r = requests.delete(self.apiURL + api)
    if r.status_code in expected_responses:
      return r
    raise Exception('Unexpected response from delete:' + api + ' (' + str(r.status_code) + ')')
  def c_put(self,api, msgData,expected_responses):
    r = requests.put(self.apiURL + api, data=json.dumps(msgData), headers={'content-type': 'application/json'})
    if r.status_code in expected_responses:
      return r
  def c_post(self,api, msgData,expected_responses):
    r = requests.put(self.apiURL + api, data=json.dumps(msgData), headers={'content-type': 'application/json'})
    if r.status_code in expected_responses:
      return r
    raise Exception('Unexpected response from post:' + api + ' (' + str(r.status_code) + ')')
    
  def getEBOList(self):
    r = self.c_get('/contents/EBOs/', [200])
    resultJSON = json.loads(r.text)
    results = []
    for curEBODir in resultJSON:
      results.append(curEBODir['name'])
    return results
  
  def _getFileFromGit(self, EBOName, Tag, FileName):  
    #r = self.c_get('/contents/EBOs/' + EBOName + '/info.json', [200])
    #resultJSON = json.loads(r.text)
    #results = []
    #print(resultJSON['download_url'])
    #Correct way to do it is to get download_url as above but I am limited to 60 calls per hour so it is better to caculate
    ## Example: https://raw.githubusercontent.com/rmetcalf9/dockPondSampleEBOs/master/EBOs/Animals/info.json
    ## API Location Example: https://api.github.com/repos/rmetcalf9/dockPondSampleEBOs
    fileURL = self.apiURL.replace('api.github.com/repos','raw.githubusercontent.com') + '/' + Tag + '/EBOs/' + EBOName + '/' + FileName
    # print(fileURL)
    with urllib.request.urlopen(fileURL) as url:
      filll = url.read().decode()
    return filll
  
  def getEBOInfoFileFromGit(self, EBOName, Tag):
    return self._getFileFromGit(EBOName, Tag, 'info.json')
    
  def getPythonModelFileFromGit(self, EBOName, Tag):
    return self._getFileFromGit(EBOName, Tag, 'model.py')
