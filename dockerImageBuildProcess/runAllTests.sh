#!/bin/bash

cd ${START_DIR}
./runUnitTests.sh
RES=$?
if [ ${RES} -ne 0 ]; then
  cd ${START_DIR}
  exit 1
fi


#No integraiton tests yet created

exit 0

