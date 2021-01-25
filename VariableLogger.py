from isy_constants import EventDispositions
from analysis import ProgramStatusAnalysis
import ObjectNameRetrieval
from isy_constants import UnitsOfMeasure
from Logger import Logger

def logVariableValue(logger, variableName, myisy):
  myisy.var_refresh_value(variableName)
  variableValue = myisy.var_get_value(variableName)
  
  message = "Tracked variable (" + variableName + ") is currently: " + str(variableValue)
  
  variableNameComponents = variableName.split("_")

  stateVariable = variableNameComponents[0] == "State"

  logObject = {
    "type": "variable",
    "object_name": variableName,
    "new_value": variableValue,
    "message": message,
    "variable_name_pieces": variableNameComponents,
    "state_variable": stateVariable
  }
  logger.logThis(logObject)
  print (message)

