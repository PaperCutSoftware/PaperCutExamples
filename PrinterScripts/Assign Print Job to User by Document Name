//
// This script is run when a new job arrives for this printer.  All code is written
// in JavaScript, and prior experience with scripting is assumed.  Use the provided
// recipes, snippets and reference documentation to assist with script development.
//
function printJobHook(inputs, actions) {
  if (!inputs.job.isAnalysisComplete) { return; }
  
  var DOC_NAME = inputs.job.documentName;  //BosaNova document name will reflect the session name (unique identifier for user)
  var DOC_NAME_LETTERS = DOC_NAME.split(/[1-9]|_/)[0].toLowerCase(); //striping session name until _ or 1-9 digits (or any regex you chose)
  var USER_NAME = inputs.job.username.toLowerCase();
  var MACHINE_NAME = inputs.job.jobSourceName.toLowerCase();
  
  if (USER_NAME === 'SERVER_ACCOUNT_NAME' && MACHINE_NAME === 'SERVER_NAME') { //used to minimize false positives and “lock” solution to specific account & machine name
    
    switch (DOC_NAME_LETTERS) {  //define your switch cases
      case 'REDUCTED_DOCUMENT_NAME_A':
        actions.job.changeUser('PAPERCUT_USER');
        break;

      case 'REDUCTED_DOCUMENT_NAME_B':
        actions.job.changeUser('PAPERCUT_USER');
        break;

      case 'REDUCTED_DOCUMENT_NAME_C':
        actions.job.changeUser('PAPERCUT_USER');
        break;
        
              
    }
    //using comments for debug 
    //actions.job.addComment(DOC_NAME + ' ' + USER_NAME + ' ' + DOC_NAME_LETTERS + ' ' + MACHINE_NAME);
  }
  
}
