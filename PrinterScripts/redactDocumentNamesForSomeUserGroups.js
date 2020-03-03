/*
Hide Document Name

Staff in the groups listed below will have document names redacted for security.

Users in these groups will have the document names removed from the
print job, but preserved in the system log. i.e. You will not be able to see the document name from the web interface.

Initially developed by the Catholic Education Archdiocese of Canberra & Goulburn
*/ 

var userGroupsForDocumentNameHiding = [ "001", "002", "003", "8000"]
var redactedName = "REDACTED"
var jobComment = "Document name redacted"

function printJobHook(inputs, actions) {

  for (g in userGroupsForDocumentNameHiding) {
    if (inputs.user.isInGroup(userGroupsForDocumentNameHiding[g])){
       // Debug messages are written to [install-path]/server/logs/server.log
       actions.log.debug("Document \"" + inputs.job.documentName + "\", Printed by: " + inputs.job.username + ", On Printer: " + inputs.job.printerName + "has been redacted")
       actions.job.changeDocumentName(redactedName)
       actions.job.addComment(jobComment)
       return
    }
  }
}

