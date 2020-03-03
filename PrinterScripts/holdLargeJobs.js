/*
* Hold jobs with a high number of pages
*
* Users printing jobs with many pages are required to manually release
* their job to confirm they meant to print such a large document
*/

function printJobHook(inputs, actions) {

  var LIMIT = 20;  // Release all jobs less than LIMIT pages

  /*
  * This print hook will need access to all job details
  * so return if full job analysis is not yet complete.
  * The only job details that are available before analysis
  * are metadata such as username, printer name, and date.
  *
  * See reference documentation for full explanation.
  */
  if (!inputs.job.isAnalysisComplete) {
    // No job details yet so return.
    return;
  }

  if (inputs.job.totalPages < LIMIT) {
    /*
    * Job is less than our page limit so release straight away
    */
    actions.job.bypassReleaseQueue()
    }
}

