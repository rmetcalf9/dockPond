# watcherThread Class
# This thread runs in the background of the app and will watch for when the app signals it has found new 
# versions of EBO's. Because of the way Flask works we need to stop and restart the application according
# to policy.
import threading
import datetime
import pytz
import time


class watcherThreadClass(threading.Thread):
  appObj = None

  running = True
  def run(self):
    self.running = True
    print('watcher thread starting')
    while self.running:
      curDatetime = datetime.datetime.now(pytz.utc)
      self.loopIteration(curDatetime)
      time.sleep(1) #one second is often enough
    print('watcher thread terminating')

  def stopThreadRunning(self):
    self.running = False

  #Once the app is setup this is called to start it watching
  def setAppObjToWatch(self, appObj):
    self.appObj = appObj

  def loopIteration(self, curDatetime):
    if self.appObj is None:
      return #No appObject setup yet to watch
    ## print('watcherthread LI')


