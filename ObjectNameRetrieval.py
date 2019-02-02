
def get_program_name(event, myisy):
  programId = event.find("eventInfo").find("id").text
  paddedProgramId = programId.rjust(4, '0')
  try:
    return myisy.prog_get_path(paddedProgramId)
  except: 
    return myisy.get_prog(paddedProgramId).name
  
def get_node_name(event, myisy):
  nodeaddress = event.find('node').text
  if nodeaddress is None:
    nodeaddress = event.find("eventInfo").text[1:13].strip()
  try:
    return myisy.node_get_path(nodeaddress)
  except: 
    return myisy._node_get_name(nodeaddress)[1]
  
def get_detailed_control(event):
  eventControlText = event.find("eventInfo").text[14:23].strip()
  return ISY.IsyEventData.EVENT_CTRL[eventControlText]
  
def get_variable_name(event, myisy):
  variableType = event.find("eventInfo").find("var").get("type")
  variableId = event.find("eventInfo").find("var").get("id")
  
  variableAddress = variableType + ":" + variableId
  return myisy.var_addrs()[variableAddress]["name"]