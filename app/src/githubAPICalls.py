import requests
import json



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
    r = self.c_get('/contents/EBOs', [200])
    resultJSON = json.loads(r.text)
    results = []
    for curEBODir in resultJSON:
      results.append(curEBODir['name'])
    return results