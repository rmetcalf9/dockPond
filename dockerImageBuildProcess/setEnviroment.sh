#!/bin/bash

export START_DIR=$(pwd)
cd ${START_DIR}
cd ../
export DOCKPOND_GITROOT=$(pwd)

cd ${START_DIR}
export CMD_PYTHONTEST=nosetests
##TODO check rednose is installed
export CMD_NPM=npm
export CMD_QUASAR=quasar
export CMD_DOCKER=docker
export CMD_GIT=git

