#!/bin/bash

#Note the following command can start a local cassandra database:
#docker run --name cassandraDB -d -p 7000:7000 -p 9042:9042 cassandra:3


APP_DIR=.

LOCAL_EXTERNHOST=localhost:3033

export APIAPP_PORT=3033
export APIAPP_MODE=DEVELOPER
export APIAPP_FRONTEND=_
export APIAPP_APIURL=http://${LOCAL_EXTERNHOST}/api
export APIAPP_APIDOCSURL=http://${LOCAL_EXTERNHOST}/apidocs
export APIAPP_APIACCESSSECURITY=[]
export APIAPP_EBOAPIURL=http://${LOCAL_EXTERNHOST}/ebos
export APIAPP_EBOAPIDOCSURL=http://${LOCAL_EXTERNHOST}/ebodocs
export APIAPP_ENVIROMENT DEV
export APIAPP_CASS_IPLIST "[ 'cassandra-1', 'cassandra-2', 'cassandra-3' ]"
export APIAPP_CASS_PORT "9042"
export APIAPP_CASS_REPLICATION "{ 'class': 'SimpleStrategy', 'replication_factor': '3' }"
export APIAPP_GITHUBREPOLOCATION "https://api.github.com/repos/rmetcalf9/dockPondSampleEBOs"

export APIAPP_VERSION=
if [ -f ${APP_DIR}/../VERSION ]; then
  APIAPP_VERSION=${0}-$(cat ${APP_DIR}/../VERSION)
fi
if [ -f ${APP_DIR}/../../VERSION ]; then
  APIAPP_VERSION=${0}-$(cat ${APP_DIR}/../../VERSION)
fi
if [ E${APIAPP_VERSION} = 'E' ]; then
  echo 'Can not find version file in standard locations'
  exit 1
fi


#Python app reads parameters from environment variables
python3 ./src/app.py
