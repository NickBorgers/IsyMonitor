try:
  import thread
except ImportError:
  import _thread as thread
import time
import json
from xml.etree.ElementTree import XML, fromstring, tostring
import websocket
import sys
sys.path.insert(0, '/usr/share/isymonitor/ISYlib-python')
import ISY
import ISY.IsyEventData
import EventDispositions
import ProgramStatusAnalysis
import ObjectNameRetrieval
import EventHandlers
import Logger

# Setup 
credentials_configruation_raw = open("~/.isy_credentials").read()

credentials_configruation = json.loads(credentials_configruation_raw)

myisy = ISY.Isy(addr="isy.nickborgers.com", userp=credentials_configruation["isy_password"], userl=credentials_configruation["isy_id"])

myheaders = {'Authorization': 'Basic ' + credentials_configruation["HTTP_Basic"], 'Sec-WebSocket-Protocol': 'ISYSUB'}

logger = new Logger()

ws = websocket.WebSocket()
# for debugging on console do:
# ws.connect("ws://isy.nickborgers.com/rest/subscribe", header=myheaders)

def on_message(ws, message):
#   print(message)
  event = fromstring(message)
  try :
    control = ISY.IsyEventData.EVENT_CTRL[(event.find('control').text)]
    control_action = ""
    try :
      control_action = ISY.IsyEventData.EVENT_CTRL_ACTION[event.find('control').text][event.find('action').text]
    except:
      control_action = None
    nodeaddress = event.find('node').text
    eventInfo = event.find("eventInfo").text

    if control is "Heartbeat" :
      print ("ISY is Alive")
    elif event.find("eventInfo").find("id") is not None :
      # This is a program execution
      EventHandlers.handleProgramEvent(logger, event, myisy)
    elif event.find("eventInfo").find("var") is not None :
      # This is a variable state change
      EventHandlers.handleVariableChange(logger, event, myisy)
    elif control not in EventDispositions.ignoredEventTypes :
      # Some other type of event has occured
      nodename = ObjectNameRetrieval.get_node_name(logger, event, myisy)
      if "Duplicate" not in nodename:
        # Some devices have extraneous nodes defined, but this event is not for a node marked as a duplicate
        if control in EventDispositions.triggerTypeEvents :
          # This is categorized as a trigger event
          EventHandlers.handleTriggerEvent(logger, event, control, control_action, nodename)
        elif control in EventDispositions.statusTypeEvents :
          # This is categorized as a status event
          EventHandlers.handleStatusEvent(logger, event, control, nodename)
        elif nodename is not None :
          # This is some other event for a known node
          EventHandlers.handleOtherNodeEvent(logger, control, node_address, nodename)
        else :
          print ("Unknown event with no parsing exception: " + control + ": " + message)
  except Exception as e :
    print ("")
    print ("Unknown event type: " + message)
    print (e)
    print ("")


def on_error(ws, error):
  print(error)

def on_close(ws):
  print("### closed ###")

def on_open(ws):
  thread.start_new_thread(run, ())

#websocket.enableTrace(True)
ws = websocket.WebSocketApp("ws://isy.nickborgers.com/rest/subscribe",
        header=myheaders,
        on_message = on_message,
        on_error = on_error,
        on_close = on_close)
ws.on_open = on_open
ws.run_forever()