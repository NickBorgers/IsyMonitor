

def extract_conditionIndicator(statusIndicator)
  return int(statusIndicator[0])
  
def extract_executionIndicator(statusIndicator)
  return int(statusIndicator[1])

def condition_status(statusIndicator):
  conditionIndicator = extract_conditionIndicator(statusIndicator)
  if conditionIndicator is 1:
    return 'unknown'
  elif conditionIndicator is 2:
    return 'true'
  elif conditionIndicator is 3:
    return 'false'
  else :
    return 'not_loaded'
    
def program_status(statusIndicator):
  executionIndicator = extract_executionIndicator(statusIndicator)
  if executionIndicator is 1:
    return 'IDLE'
  elif executionIndicator is 2:
    return'running THEN'
  elif executionIndicator is 3:
    return 'running ELSE'