//$ per year color limit
//
// Created by Michael Tomlinson <michael.tomlinson@acd-inc.com>
//
function printJobHook(inputs, actions){

  // Modify this value to change the color cost limit.  
  var MAX_COLOR_AMOUNT_PER_YEAR = 25.00;
  // Modify this vaule to change the color cost per page
  var COLOR_PAGE_COST = .1;

  //user-defined properties
  var currentColorCount = inputs.user.getNumberProperty("current-color-count");
  var yearLastSeen = inputs.user.getProperty("color-year-last-seen");

  if (!inputs.job.isAnalysisComplete) {
    return;
  }//analysis complete

  if (!inputs.job.isColor) {
    // Not color so no need to check and apply any limits.
    return;
  }

  if (currentColorCount == null) { 
    currentColorCount = 0;
  }

  var currentDate = inputs.job.date;
  var tempDate = currentDate.toDateString();
  var currentYearIndex = tempDate.slice(10, 15); 

  if (yearLastSeen == null || yearLastSeen != currentYearIndex) {
    // It's a new year. Reset the current count value to zero.
    //actions.log.debug("Reset color counter for " + inputs.job.username);
    currentColorCount = 0;
  }

  //magic!
  var tempColorCount = inputs.job.totalColorPages * COLOR_PAGE_COST;

  if (currentColorCount + tempColorCount >= MAX_COLOR_AMOUNT_PER_YEAR) {
    var deniedMessage = "This print job has been denied.  You have exceeded"
        + " your limit of " + inputs.utils.formatCost(MAX_COLOR_AMOUNT_PER_YEAR)
        + ". Please print in grayscale.";
    actions.client.sendMessage(deniedMessage);
    actions.job.cancelAndLog("This job was denied because you have exceeded"
                             + " the color quota.");
    //actions.log.debug("User " + inputs.job.username + " has ran out of color prints");
    return;

  }

  // If we're here, it's OK to process the job
  // Save the current count
  currentColorCount += tempColorCount;
  actions.user.onCompletionSaveProperty("current-color-count", currentColorCount, {saveWhenCancelled:true});
  actions.user.onCompletionSaveProperty("color-year-last-seen", currentYearIndex);

}//end printJobHook
