#!/bin/bash

#Note the following command can start a local cassandra database:
#docker run --name cassandraDB -d -p 7000:7000 -p 9042:9042 cassandra:3


APP_DIR=.

export APIAPP_PORT=3033
export APIAPP_MODE=DEVELOPER
export APIAPP_FRONTEND=_
export APIAPP_APIURL=http://localhost/api
export APIAPP_APIDOCSURL=http://localhost/apidocs/
export APIAPP_APIACCESSSECURITY=[]

export APIAPP_ENVIROMENT=DEV
export APIAPP_CASS_IPLIST="[ 'localhost' ]"
export APIAPP_CASS_PORT="9042"
export APIAPP_CASS_REPLICATION="{ 'class': 'SimpleStrategy', 'replication_factor': '1' }"


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
