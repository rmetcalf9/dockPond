# DockPond

TODO

I put images for this project into the [Docker hub](https://hub.docker.com/r/metcarob/dockpond/)

# Features

TODO

# Getting started - Running DockPond to check it out...

TODO

# Contributing

If you have any ideas, just open an issue and tell me what you think.


## My release process

At the moment I have a multi stage build so it wasn't possible to use TravisCI to make an automatic build process.

To release dockpond I:
 - Run the [build process](./dockerImageBuildProcess/README.md) to create an image on my local machine
 - Make sure I remember to stop the dev server instances before testing the container
 - Launch the image with a docker run command and make sure it starts and the logs display correct version number
 - *** compose test possibly portainer
 - When testing usg incognito mode as the webapp is cached by browsers.
 - Rename milestone to match release
 - Update RELEASE.md (pointing at the milestone)
 - Run docker login and log in to my docker hub account
 - Run docker push metcarob/dockpond:VERSION (Replace VERSION with version number that was just built)
 - Run docker push metcarob/dockpond:latest
 - Create new next milestone

# Related projects

Here's a list of other related projects:
 - [dockJob](https://github.com/rmetcalf9/dockJob)
 - [Kong](https://konghq.com/)
 - [Konga](https://github.com/pantsel/konga)
 - [Quasar Framework](http://quasar-framework.org/)
 - [baseapp_for_restapi_backend_with_swagger](https://github.com/rmetcalf9/baseapp_for_restapi_backend_with_swagger) - My own library of shared utilities created so I can use this method of making API backends mutiple times.