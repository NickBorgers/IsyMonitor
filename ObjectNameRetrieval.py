
def get_program_name(event, myisy):
  programId = event.find("eventInfo").find("id").text
  paddedProgramId = programId.rjust(4, '0')
  return myisy.get_prog(paddedProgramId).name