from TestHelperSuperClass import testHelperAPIClient
import unittest
import json
from unittest.mock import patch, call

#This file is for testing various models that may be used

basic_model_str = "from flask_restplus import fields\n\ndef getModel(flaskRestPlusAPI):\n  return flaskRestPlusAPI.model('Animal', {\n      'name': fields.String(default='',description='What is the name of this animal? (Must be unique)')\n  })"

complex_model_str = "from flask_restplus import fields\n\ndef getModel(flaskRestPlusAPI):\n  def getTypeModel(flaskRestPlusAPI, typeName):\n    if typeName=='ABC':\n      return flaskRestPlusAPI.model('ABC', {\n          'Nname': fields.String(default='',description='What is the name of this animal? (Must be unique)'),\n          'Ttype': fields.String(default='',description='What type of animal are they?'),\n          'HHatedByRobert': fields.Boolean(default=False,description='Does Robert hate this animal?')\n      })\n    if typeName=='DEF':\n      return flaskRestPlusAPI.model('DEF', {\n          'Nname': fields.String(default='',description='What is the name of this animal? (Must be unique)'),\n          'Nname2222': fields.String(default='',description='What is the name of this animal? (Must be unique)')\n      })\n    raise Exception('Searching for unknown type')\n  return flaskRestPlusAPI.model('Animal', {\n      'name': fields.String(default='',description='What is the name of this animal? (Must be unique)'),\n      'type': fields.String(default='',description='What type of animal are they?'),\n      'HatedByRobert': fields.Boolean(default=False,description='Does Robert hate this animal?'),\n      'TestNestedStructure': fields.Nested(getTypeModel(flaskRestPlusAPI, 'ABC')),\n      'TestListStructure': fields.List(fields.String(default='',description='list item')),\n      'TestNestedListStructure': fields.List(fields.Nested(getTypeModel(flaskRestPlusAPI, 'DEF')))\n  })\n\n"


class test_modelCode(testHelperAPIClient):

  @patch('githubAPICalls.githubAPICallsClass.getEBOList', return_value=[ 'AnimalsV1' ])
  @patch('githubAPICalls.githubAPICallsClass.getEBOInfoFileFromGit', return_value='{"Deployments": {"DEV_INT_TEST": "0.0.1"}}')
  @patch('githubAPICalls.githubAPICallsClass.getPythonModelFileFromGit', return_value=basic_model_str)
  def test_getEBOs(self, getEBOListCall, getEBOInfoFileFromGit1, getEBOInfoFileFromGit2):
    self.setUpMAN()
    expRes = {
      "pagination": {
        "offset": 0, "pagesize": 100, "total": 1
       }, 
       "result": [
        {"name": "AnimalsV1"}
       ]
      }
    result = self.testClient.get('/api/EBOs/')
    self.assertEqual(result.status_code, 200)
    resultJSON = json.loads(result.get_data(as_text=True))
    self.assertJSONStringsEqual(resultJSON['pagination'], expRes['pagination'], msg="Pagination part wrong")
    matchedARR = list(expRes['result'])
    numMatched = 0
    for returnedIdx, returnedVal in enumerate(resultJSON['result']):
      for idx, val in enumerate(matchedARR):
        # print(val['name'])
        # print(returnedVal['name'])
        if val['name'] == returnedVal['name']:
          matchedARR[idx] = {"name": "_"}
          numMatched = numMatched + 1
          print(returnedVal['errorStateReason'])
          self.assertEqual(returnedVal['state'],'OK', msg=returnedVal['name'] + ' API found but state != OK (it was ' + returnedVal['state'] + ')')
    self.assertEqual(len(matchedARR),numMatched,msg='Didn\'t match all results')

  @patch('githubAPICalls.githubAPICallsClass.getEBOList', return_value=[ 'AnimalsV1' ])
  @patch('githubAPICalls.githubAPICallsClass.getEBOInfoFileFromGit', return_value='{"Deployments": {"DEV_INT_TEST": "0.0.1"}}')
  @patch('githubAPICalls.githubAPICallsClass.getPythonModelFileFromGit', return_value=complex_model_str)
  def test_complexModel(self, getEBOListCall, getEBOInfoFileFromGit1, getEBOInfoFileFromGit2):
    self.setUpMAN()
    expRes = {
      "pagination": {
        "offset": 0, "pagesize": 100, "total": 1
       }, 
       "result": [
        {"name": "AnimalsV1"}
       ]
      }
    result = self.testClient.get('/api/EBOs/')
    self.assertEqual(result.status_code, 200)
    resultJSON = json.loads(result.get_data(as_text=True))
    self.assertJSONStringsEqual(resultJSON['pagination'], expRes['pagination'], msg="Pagination part wrong")
    matchedARR = list(expRes['result'])
    numMatched = 0
    for returnedIdx, returnedVal in enumerate(resultJSON['result']):
      for idx, val in enumerate(matchedARR):
        # print(val['name'])
        # print(returnedVal['name'])
        if val['name'] == returnedVal['name']:
          matchedARR[idx] = {"name": "_"}
          numMatched = numMatched + 1
          print(returnedVal['errorStateReason'])
          self.assertEqual(returnedVal['state'],'OK', msg=returnedVal['name'] + ' API found but state != OK (it was ' + returnedVal['state'] + ')')
    self.assertEqual(len(matchedARR),numMatched,msg='Didn\'t match all results')

