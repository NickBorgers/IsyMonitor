from isy_constants import EventDispositions
from analysis import ProgramStatusAnalysis
import ObjectNameRetrieval
from isy_constants import UnitsOfMeasure
from Logger import Logger

def handleProgramEvent(logger, event, myisy):
  try:
    statusIndicator = event.find("eventInfo").find("s").text
    conditionStatus = ProgramStatusAnalysis.condition_status(statusIndicator)
    programStatus = ProgramStatusAnalysis.program_status(statusIndicator)
  except: 
    statusIndicator = 'unknown'
    conditionStatus = 'unknown'
    programStatus = 'unknown'

  if conditionStatus is 'false' and programStatus is 'IDLE':
    #Ignore a program that's not running
    pass
  if conditionStatus is 'unknown' and programStatus is 'unknown':
    #Ignore this report because I don't what it means and they are noisy in the logs
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
      
  variableNewValueString = event.find("eventInfo").find("var").find("val").text
  variableNewValue = int(variableNewValueString, 10)
  
  message = "Variable (" + variableName + ") is now: " + variableNewValueString

  variableNameComponents = variableName.split("_")
  stateVariable = variableNameComponents[0] == "State"
  
  logObject = {
    "type": "variable",
    "object_name": variableName,
    "new_value": variableNewValue,
    "message": message,
    "node_address": getNodeAddress(event),
    "variable_name_pieces": variableNameComponents,
    "state_variable": stateVariable
  }
  logger.logThis(logObject)
  print (message)
  
def handleTriggerEvent(logger, event, control, control_action, nodename):
  try :
    # attempt to get more detailed control event description from within the event info
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
    # Cleanse Status Detail of any degree character
    statusDetail = statusDetail.split(u'\u00B0',1)[0]
    message = "Status (" + control + ") of: " + nodename + " is: " + statusDetail
    # Interpret unit of measure
    unitOfMeasureIndex = int(event.find("action").get("uom"))
    unitOfMeasure = UnitsOfMeasure.unitsOfMeasure[unitOfMeasureIndex]
    # Do common object construction:
    logObject = {
        "type": "status",
        "object_name": nodename,
        "attribute" : control,
        "status_detail": statusDetail,
        "message": message,
        "node_address": getNodeAddress(event),
        "object_folder_path": getPath(nodename),
        "unit_of_measure": unitOfMeasure
    }

    # Handle special cases of temp reporting and humidity
    if unitOfMeasure in UnitsOfMeasure.temperatureUnitsOfMeasure:
      logObject["temperature"] = {
        "units": unitOfMeasure,
        "degrees": float(statusDetail)
      }

    if "relative humidity" in unitOfMeasure:
      logObject["relative_humidity"] = int(statusDetail.replace("%",""))

    logger.logThis(logObject)
    print (message)
  else:
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
