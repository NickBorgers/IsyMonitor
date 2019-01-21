import json
from Queue import Queue

class Logger:

  logMessageQueue = Queue()

  def __init__(self):
    logging_configuration_raw = open("log.conf").read()
    logging_configuration = json.loads(logging_configuration_raw)
    
    self.logFile = open(logging_configuration["dest_file"], "a")
    
    print("Logger ready to log JSON objects to " + logging_configuration["dest_file"])

  def logThis(self, objectToLog):
    logMessageQueue.put(objectToLog)
    if logMessageQueue.size() > 3 :
      flushLogQueue()
    
  def flushLogQueue():
    while logMessageQueue.qsize():
      self.logFile.write(json.dumps(objectToLog) + "\n")