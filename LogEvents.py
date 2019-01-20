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

credentials_configruation_raw = open("/usr/share/isymonitor/.isy_credentials").read()

credentials_configruation = json.loads(credentials_configruation_raw)

myisy = ISY.Isy(addr="isy.nickborgers.com", userp=credentials_configruation["isy_password"], userl=credentials_configruation["isy_id"])

myheaders = {'Authorization': 'Basic ' + credentials_configruation["HTTP_Basic"], 'Sec-WebSocket-Protocol': 'ISYSUB'}

ws = websocket.WebSocket()
#ws.connect("ws://isy.nickborgers.com/rest/subscribe", header=myheaders)

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
    elif control_action == "Var Stat" :
      print ("Variable status: " + event.find("eventInfo").text)
    elif event.find("eventInfo").find("id") is not None :
      # This is a program execution
      statusIndicator = event.find("eventInfo").find("s").text

      conditionStatus = ProgramStatusAnalysis.condition_status(statusIndicator)
      programStatus = ProgramStatusAnalysis.program_status(statusIndicator)

      if conditionStatus is 'false' and programStatus is 'IDLE':
        pass
      else:
        programName = ObjectNameRetrieval.get_program_name(event, myisy)
        print ("Program (" + programName + ") is (" + statusIndicator + ") " + programStatus + " with condition " + conditionStatus)
    elif control not in EventDispositions.ignoredEventTypes :
      nodename = ObjectNameRetrieval.get_node_name(event, myisy)
      if control in EventDispositions.triggerTypeEvents :
        if "Duplicate" not in nodename:
          try :
            control = get_detailed_control(event)
          except:
            pass
          if control not in EventDispositions.ignoredEventTypes :
            if control_action is not None:
              print (control + " by: " + nodename + " : " + control_action)
            else:
              print (control + " by: " + nodename)
      elif control in EventDispositions.statusTypeEvents :
        if nodeaddress is not None :
          if "Duplicate" not in nodename:
            statusDetail = event.find("fmtAct").text
            print ("Status (" + control + ") of: " + nodename + " is: " + statusDetail)
        else :
          print ("Got statusTypeEvent but no nodeaddress")
      elif nodeaddress is not None :
        # Known node status
        if nodename is not "Duplicate":
          print (control + " : " + nodeaddress + ": " + nodename)
          print (message)
          print ("")
      elif event.find("eventInfo") is not None :
        if event.find("eventInfo").find("value") is None :
          try :
            print (control + " : " + eventInfo + ": " + nodename)
            print ("")
          except:
            print (control + " : " + tostring(event))
        else :
          print (control + " : " + tostring(event))
    else :
      print (control + " : " + tostring(event))
  except Exception as e :
    print ("Unknown event type:" + tostring(event))
    print (e)
    print ("")


def on_error(ws, error):
  print(error)

def on_close(ws):
  print("### closed ###")

def on_open(ws):
  thread.start_new_thread(run, ())

def get_control_number_string(controlNumber):
  switcher = {
    "_0": "Hearbeat",
    "_11": "Weather Report",
    "_19": "ELK Event",
    "_21": "Z-wave Event",
    "_22": "Power usage report"
  }
  return switcher.get(controlNumber, controlNumber)

#websocket.enableTrace(True)
ws = websocket.WebSocketApp("ws://isy.nickborgers.com/rest/subscribe",
        header=myheaders,
        on_message = on_message,
        on_error = on_error,
        on_close = on_close)
ws.on_open = on_open
ws.run_forever()

