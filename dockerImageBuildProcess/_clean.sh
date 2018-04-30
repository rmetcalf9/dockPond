#!/bin/bash

source ./setEnviroment.sh

echo "Executing Quasar webfrontend build"
cd ${DOCKPOND_GITROOT}/webfrontend
eval ${CMD_QUASAR} clean
RES=$?
if [ ${RES} -ne 0 ]; then
  cd ${START_DIR}
  echo ""
  echo "Quasar clean failed"
  exit 1
fi

rm -rf ${DOCKPOND_GITROOT}/webfrontend/dist
RES=$?
if [ ${RES} -ne 0 ]; then
  cd ${START_DIR}
  exit 1
fi

exit 0

