import EventDispositions
import ProgramStatusAnalysis
import ObjectNameRetrieval

def handleProgramEvent(event, myisy):
  statusIndicator = event.find("eventInfo").find("s").text

  conditionStatus = ProgramStatusAnalysis.condition_status(statusIndicator)
  programStatus = ProgramStatusAnalysis.program_status(statusIndicator)

  if conditionStatus is 'false' and programStatus is 'IDLE':
    #Ignore a program that's not running
    pass
  else:
    programName = ObjectNameRetrieval.get_program_name(event, myisy)
    print ("Program (" + programName + ") is (" + statusIndicator + ") " + programStatus + " with condition " + conditionStatus)
    
    
def handleVariableChange(event, myisy):
  variableName = ObjectNameRetrieval.get_variable_name(event, myisy)
      
  variableNewValue = event.find("eventInfo").find("var").find("val").text
    
  print ("Variable (" + variableName + ") is now: " + variableNewValue)
  
def handleTriggerEvent(event, control, control_action, nodename):
  try :
    # attempt to get more deetailed control event description from within the event info
    control = ObjectNameRetrieval.get_detailed_control(event)
  except:
    pass
  if control not in EventDispositions.ignoredEventTypes :
    if control_action is not None:
      if control_action != 'Info String' :
        print (control + " by: " + nodename + " : " + control_action)
    else:
      print (control + " by: " + nodename)
        
def handleStatusEvent(event, control, nodename):
  if nodename is not None :
    statusDetail = event.find("fmtAct").text
    print ("Status (" + control + ") of: " + nodename + " is: " + statusDetail)
  else :
    print ("Status (no nodename could be determined)")
    
def handleOtherNodeEvent(control, node_address, nodename):
  print ("Other event type for known node: " + control + " : " + nodeaddress + ": " + nodename)