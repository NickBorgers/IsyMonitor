import json

class Logger:

  def __init__(self):
    logging_configuration_raw = open("log.conf").read()
    logging_configuration = json.loads(logging_configuration_raw)
    
    self.logFile = open(logging_configuration["dest_file"], "a", buffering=1)
    
    print("Logger ready to log JSON objects to " + logging_configuration["dest_file"])

  def logThis(self, objectToLog):
    self.logFile.write(json.dumps(objectToLog) + "\n")
