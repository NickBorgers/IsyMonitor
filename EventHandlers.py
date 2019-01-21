import EventDispositions
import ProgramStatusAnalysis
import ObjectNameRetrieval
import Logger from Logger

def handleProgramEvent(logger, event, myisy):
  statusIndicator = event.find("eventInfo").find("s").text

  conditionStatus = ProgramStatusAnalysis.condition_status(statusIndicator)
  programStatus = ProgramStatusAnalysis.program_status(statusIndicator)

  if conditionStatus is 'false' and programStatus is 'IDLE':
    #Ignore a program that's not running
    pass
  else:
    programName = ObjectNameRetrieval.get_program_name(event, myisy)
    logObject = {
      "type": "program",
      "object_name": programName,
      "new_status" : programStatus,
      "condition": conditionStatus,
      "status_detail": statusIndicator
    }
    logger.logThis(logObject)
    print ("Program (" + programName + ") is (" + statusIndicator + ") " + programStatus + " with condition " + conditionStatus)
    
    
def handleVariableChange(logger, event, myisy):
  variableName = ObjectNameRetrieval.get_variable_name(event, myisy)
      
  variableNewValue = event.find("eventInfo").find("var").find("val").text
    
  logObject = {
    "type": "variable",
    "object_name": variableName,
    "new_status" : variableNewValue,
  }
  logger.logThis(logObject)
  print ("Variable (" + variableName + ") is now: " + variableNewValue)
  
def handleTriggerEvent(logger, event, control, control_action, nodename):
  try :
    # attempt to get more deetailed control event description from within the event info
    control = ObjectNameRetrieval.get_detailed_control(event)
  except:
    pass
  if control not in EventDispositions.ignoredEventTypes :
    if control_action is not None:
      if control_action != 'Info String' :
        logObject = {
          "type": "program",
          "object_name": nodename,
          "new_status" : control,
          "status_detail": control_action
        }
        logger.logThis(logObject)
        print (control + " by: " + nodename + " : " + control_action)
    else:
      logObject = {
        "type": "program",
        "object_name": nodename,
        "new_status" : control,
      }
      logger.logThis(logObject)
      print (control + " by: " + nodename)
        
def handleStatusEvent(logger, event, control, nodename):
  if nodename is not None :
    statusDetail = event.find("fmtAct").text
    logObject = {
      "type": "program",
      "object_name": nodename,
      "new_status" : control,
      "status_detail": statusDetail
    }
    logger.logThis(logObject)
    print ("Status (" + control + ") of: " + nodename + " is: " + statusDetail)
  else :
    logObject = {
      "type": "program",
      "object_name": "unknown",
      "new_status" : control
    }
    logger.logThis(logObject)
    print ("Status (no nodename could be determined)")
    
def handleOtherNodeEvent(logger, control, node_address, nodename):
  logObject = {
    "type": "other",
    "object_name": nodeaddress,
    "new_status" : control
  }
  logger.logThis(logObject)
  print ("Other event type for known node: " + control + " : " + nodeaddress + ": " + nodename)