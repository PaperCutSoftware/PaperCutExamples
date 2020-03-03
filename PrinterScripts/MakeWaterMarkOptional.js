/*
* Provide the user with opportunity to remove watermark before printing
*
* The default watermark are used unless the users enters a valid override code
*/

var OVERRIDE_CODE = "Plain"

function printJobHook(inputs, actions) {

  var response = actions.client.promptForText("Please the enter appropriate code to remove watermarking:",{"defaultText": "Watermark"});

  if (response  == "TIMEOUT" || response == "CANCEL") {
    // Timed out, so cancel the job and exit script.
    actions.job.cancel();
    return;
  }

  if (response  == OVERRIDE_CODE ) {
    actions.job.setWatermark("");
  } // else  use configured defaults
}
