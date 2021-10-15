import threading
import time
import json
from xml.etree.ElementTree import XML, fromstring, tostring
import websocket
import sys
sys.path.insert(0, '/usr/share/isymonitor/ISYlib-python')
import ISY
import ISY.IsyEventData
import VariableLogger
from Logger import Logger
import os

# Setup 
credentials_configruation_raw = open(os.path.expanduser("~/.isy_credentials")).read()

credentials_configruation = json.loads(credentials_configruation_raw)

myisy = ISY.Isy(addr="isy.nickborgers.com", userp=credentials_configruation["isy_password"], userl=credentials_configruation["isy_id"])

logger = Logger()

def log_all_variables():
  for var in myisy.var_addrs():
    VariableLogger.logVariableValue(logger, myisy.var_addrs()[var]["name"], myisy)
  print("Logged variables")

while True:
  thread = threading.Thread(target=log_all_variables)
  thread.start()
  time.sleep(60)
