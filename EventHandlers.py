import EventDispositions
import ProgramStatusAnalysis
import ObjectNameRetrieval
from Logger import Logger

def handleProgramEvent(logger, event, myisy):
  try:
    statusIndicator = event.find("eventInfo").find("s").text
    conditionStatus = ProgramStatusAnalysis.condition_status(statusIndicator)
    programStatus = ProgramStatusAnalysis.program_status(statusIndicator)
  except: 
    conditionStatus = 'unknown'
    programStatus = 'unknown'

  if conditionStatus is 'false' and programStatus is 'IDLE':
    #Ignore a program that's not running
    pass
  else:
    programName = ObjectNameRetrieval.get_program_name(event, myisy)
    message = "Program (" + programName + ") is (" + statusIndicator + ") " + programStatus + " with condition " + conditionStatus
    logObject = {
      "type": "program",
      "object_name": programName,
      "new_status" : programStatus,
      "condition": conditionStatus,
      "status_detail": statusIndicator,
      "message": message,
      "node_address": getNodeAddress(event),
      "object_folder_path": getPath(programName)
    }
    logger.logThis(logObject)
    print (message)
    
    
def handleVariableChange(logger, event, myisy):
  variableName = ObjectNameRetrieval.get_variable_name(event, myisy)
      
  variableNewValue = event.find("eventInfo").find("var").find("val").text
  
  message = "Variable (" + variableName + ") is now: " + variableNewValue
  
  logObject = {
    "type": "variable",
    "object_name": variableName,
    "new_status": variableNewValue,
    "message": message,
    "node_address": getNodeAddress(event)
  }
  logger.logThis(logObject)
  print (message)
  
def handleTriggerEvent(logger, event, control, control_action, nodename):
  try :
    # attempt to get more deetailed control event description from within the event info
    control = ObjectNameRetrieval.get_detailed_control(event)
  except:
    pass
  if control not in EventDispositions.ignoredEventTypes :
    if control_action is not None:
      if control_action != 'Info String' :
        message = control + " by: " + nodename + " : " + control_action
        logObject = {
          "type": "trigger",
          "object_name": nodename,
          "new_status" : control,
          "status_detail": control_action,
          "message": message,
          "node_address": getNodeAddress(event),
          "object_folder_path": getPath(nodename)
        }
        logger.logThis(logObject)
        print (message)
    else:
      message = control + " by: " + nodename
      logObject = {
        "type": "trigger",
        "object_name": nodename,
        "new_status" : control,
        "message": message,
        "node_address": getNodeAddress(event),
        "object_folder_path": getPath(nodename)
      }
      logger.logThis(logObject)
      print (message)
        
def handleStatusEvent(logger, event, control, nodename):
  if nodename is not None :
    statusDetail = event.find("fmtAct").text
    message = "Status (" + control + ") of: " + nodename + " is: " + statusDetail
    # Handle special case of thermostat
    if (control is "Thermostat Reading") :
      logObject = {
        "type": "status",
        "object_name": nodename,
        "attribute" : control,
        "status_detail": statusDetail,
        "message": message,
        "node_address": getNodeAddress(event),
        "object_folder_path": getPath(nodename),
        # Strip units from temperature
        "temperatureDegrees": statusDetail.split("°",1)[0]
      }
      logger.logThis(logObject)
      print (message)
    else :
      logObject = {
        "type": "status",
        "object_name": nodename,
        "attribute" : control,
        "status_detail": statusDetail,
        "message": message,
        "node_address": getNodeAddress(event),
        "object_folder_path": getPath(nodename)
      }
      logger.logThis(logObject)
      print (message)
  else :
    message = "Status (no nodename could be determined)"
    logObject = {
      "type": "status",
      "object_name": "unknown",
      "new_status": control,
      "message": message,
      "node_address": getNodeAddress(event)
    }
    logger.logThis(logObject)
    print (message)
    
def handleOtherNodeEvent(logger, control, node_address, nodename):
  message = "Other event type for known node: " + control + " : " + node_address + ": " + nodename
  logObject = {
    "type": "other",
    "object_name": node_address,
    "new_status": control,
    "message": message,
    "node_address": node_address,
    "object_folder_path": getPath(nodename)
  }
  logger.logThis(logObject)
  print (message)
  
def getNodeAddress(event):
  try:
    return event.find('node').text
  except:
    return 'None'
    
def getPath(name):
  pathFolders = name.split("/")[1:]
  path = {}
  folderNum=1
  for thisPathFolder in pathFolders:
    path["Folder" + str(folderNum)] = thisPathFolder
    folderNum += 1
  return path
