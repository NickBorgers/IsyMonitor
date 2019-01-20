
def condition_status(conditionIndicator):
  if conditionIndicator is 1:
    return 'unknown'
  elif conditionIndicator is 2:
    return 'true'
  elif conditionIndicator is 3:
    return 'false'
  else :
    return 'not_loaded'