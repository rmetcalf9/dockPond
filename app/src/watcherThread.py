# watcherThread Class
# This thread runs in the background of the app and will watch for when the app signals it has found new 
# versions of EBO's. Because of the way Flask works we need to stop and restart the application according
# to policy.
import threading
import datetime
import pytz
import time
import traceback
import sys


class watcherThreadClass(threading.Thread):
  appObj = None

  reloadRequested = False
  activityLock = threading.Lock()

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
    try:
      if self.appObj is None:
        return #No appObject setup yet to watch
      if self.reloadRequested:
        self.activityLock.acquire()
        self.reloadRequested = False
        self.appObj.reloadAPIsFromGithub()
        self.activityLock.release()
    except Exception as e:
      print("Exception in watcher thread")
      exc_type, exc_value, exc_traceback = sys.exc_info()
      traceback.print_exception(exc_type, exc_value, exc_traceback,limit=8, file=sys.stdout)
      # We may have activity lock aquired so release it so thread keeps running
      self.activityLock.release()
    ## print('watcherthread LI')

  def requestReload(self):
    self.activityLock.acquire()
    if self.reloadRequested:
      self.activityLock.release()
      return ("Already requested", 200)
    self.reloadRequested = True
    self.activityLock.release()
    return ("Requested logged", 200)

