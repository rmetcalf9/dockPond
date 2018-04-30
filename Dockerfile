FROM alpine

MAINTAINER Robert Metcalf

RUN apk add --no-cache bash python3 curl && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    rm -r /root/.cache && \
    pip3 install --upgrade pip

ENV APP_DIR /app
ENV APIAPP_FRONTEND /webfrontend
ENV APIAPP_APIURL http://localhost:80/dockpondapi
ENV APIAPP_APIDOCSURL http://localhost:80/apidocs
ENV APIAPP_APIACCESSSECURITY '[]'


# APIAPP_MODE is not definable here as it is hardcoded to DOCKER in the shell script
# APIAPP_VERSION is not definable here as it is read from the VERSION file inside the image

EXPOSE 80

RUN \
  mkdir ${APP_DIR} && \
  mkdir ${APIAPP_FRONTEND}


COPY ./app/src ${APP_DIR}
RUN pip3 install -r ${APP_DIR}/requirments.txt

COPY ./webfrontend/dist/spa-mat ${APIAPP_FRONTEND}

COPY ./VERSION /VERSION

COPY ./app/run_app_docker.sh /run_app_docker.sh

CMD ["/run_app_docker.sh"]

# Regular checks. Docker won't send traffic to container until it is healthy
#  and when it first starts it won't check the health until the interval so I can't have
#  a higher value without increasing the startup time
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://127.0.0.1:80/frontend/index.html || exit 1

##docker run --name dockpond -p 80:80 -d metcarob/dockpond:latest