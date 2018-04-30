#!/bin/bash

source ./setEnviroment.sh

# Script designed to remove all local dockjob images

ii=$(docker images | grep metcarob/dockpond)
if [ 0 -eq ${#ii} ]; then
  echo 'No metcarob/dockpond images present'
  exit 0
fi

docker images -a | grep "metcarob/dockpond" | awk '{print $3}' | xargs docker rmi -f
#docker system prune -a -f
RES=$?
if [ ${RES} -ne 0 ]; then
  cd ${START_DIR}
  echo 'ERROR'
  exit 1
fi

ii=$(docker images | grep metcarob/dockpond)
if [ 0 -ne ${#ii} ]; then
  echo '\nError metcarob/dockpond images remain'
  exit 1
fi

echo '\n${0} completed sucessfully'

exit 0

