
def get_program_name(event, myisy):
  programId = event.find("eventInfo").find("id").text
  paddedProgramId = programId.rjust(4, '0')
  return myisy.get_prog(paddedProgramId).name
  
def get_node_name(event, myisy):
  if nodeaddress is None:
    nodeaddress = event.find("eventInfo").text[1:13].strip()
  return myisy._node_get_name(nodeaddress)[1]