
def get_program_name(event, myisy):
  programId = event.find("eventInfo").find("id").text
  paddedProgramId = programId.rjust(4, '0')
  return myisy.prog_get_path(paddedProgramId)
  
def get_node_name(event, myisy):
  nodeaddress = event.find('node').text
  if nodeaddress is None:
    nodeaddress = event.find("eventInfo").text[1:13].strip()
  return myisy.node_get_path(nodeaddress)
  
def get_detailed_control(event):
  eventControlText = event.find("eventInfo").text[14:23].strip()
  return ISY.IsyEventData.EVENT_CTRL[eventControlText]
  
def get_variable_name(event, myisy):
  variableType = event.find("eventInfo").find("var").get("type")
  variableId = event.find("eventInfo").find("var").get("id")
  
  variableAddress = variableType + ":" + variableId
  return myisy.var_addrs()[variableAddress]["name"]