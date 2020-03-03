// Staircase / color quota script

// Some organisations like to be able to provide one rate for pages under a certain
// threshold and then a higher rate for pages that exceed this threshold. The
// counters are reset each month.


// The logic of this script can also be easily adapted to cancel jobs that push over
// a threshold rather than just adjust their pricing. i.e. if the organisation
// wants to keep the utilization of a machine to a 'total number of pages per
// month/quarter/year' to ensure they don't exceed their best rate on the machine,
// it would be a very easy change.

//
function printJobHook(inputs, actions) {
  
  if (!inputs.job.isAnalysisComplete) {
    // No job details yet so return.
    return;
  }
  
  //Create a year-month string as my**Key for both color and mono pages tracking
  var d = new Date();
  var y = d.getFullYear();
  var m = d.getMonth();
  var myMonoKey =  "Mono: " + y + "-" + m;
  var myColorKey = "Color: " + y + "-" + m;
  var monoKeyExists = true;
  var colorKeyExists = true;
  
  //Define the number of prints at which we need to start applying a new price
  var thresholdMonoPrints = 12;
  var thresholdColorPrints = 16;
  
  //Get the number of color and mono prints for this queue, for this month so far
  var monoPrintsThisMonth = inputs.printer.getNumberProperty(myMonoKey);
  var colorPrintsThisMonth = inputs.printer.getNumberProperty(myColorKey);
  
  if (monoPrintsThisMonth == null) {
    monoKeyExists=false;
    monoPrintsThisMonth=0;
  }
  
  // We don't expect to have mono key but not color key (and vice-vera) but just to be on the safe side...
  if (colorPrintsThisMonth == null) {
    colorKeyExists=false;
    colorPrintsThisMonth=0;
  }
  
  //Define the low and high costs for mono and color pages
  var lowMonoCost = .05;
  var highMonoCost = .20;
  var lowColorCost = .50;
  var highColorCost = 1.00;
  
  
  //Define the variables for the job cost elements
  var monoPagesJobCost = 0;
  var colorPagesJobCost = 0;
  
  var colorPagesOver = 0;
  var monoPagesOver = 0;
  
  actions.log.debug("This month's stats: (color pages/threshold):"+colorPrintsThisMonth+"/"+thresholdColorPrints+" , (mono pages/threshold):"+monoPrintsThisMonth+"/"+thresholdMonoPrints);
  //Workout the color pages job cost
  if(colorPrintsThisMonth > thresholdColorPrints)
  {
    //If the pages this month already exceed the threshold, charge them all at the high rate
    colorPagesJobCost = inputs.job.totalColorPages * highColorCost;
    colorPagesOver = inputs.job.totalColorPages;
  }
  else if ((colorPrintsThisMonth + inputs.job.totalColorPages) <= thresholdColorPrints)
  {
    //If the pages this month PLUS the total color pages for this job are under the threshold, charge them all at the lower rate
    colorPagesJobCost = inputs.job.totalColorPages * lowColorCost;
  }
  else
  {
    //This job will have some pages at the lower, and some at the higher rate
    
    //The pages over the threshold are the number of pages so far this month, plus these pages MINUS the threshold
    colorPagesOver = (colorPrintsThisMonth + inputs.job.totalColorPages) - thresholdColorPrints;
    
    //The pages under then are the pages in this job, less the pages over
    var colorPagesUnder = inputs.job.totalColorPages - colorPagesOver;
    
    //And the cost of the job is the combination of the over pages and the high rate, and the pages under and the low rate
    colorPagesJobCost = (colorPagesOver * highColorCost) + (colorPagesUnder * lowColorCost);
  }
  
  
  //Workout the mono pages job cost
  if(monoPrintsThisMonth > thresholdMonoPrints)
  {
    //If the pages this month already exceed the threshold, charge them all at the high rate
    monoPagesJobCost = inputs.job.totalGrayscalePages * highMonoCost;
    monoPagesOver = inputs.job.totalMonoPages;
  }
  else if ((monoPrintsThisMonth + inputs.job.totalGrayscalePages) <= thresholdMonoPrints)
  {
    //If the pages this month PLUS the total mono pages for this job are under the threshold, charge them all at the lower rate
    monoPagesJobCost = inputs.job.totalGrayscalePages * lowMonoCost;
  }
  else
  {
    //This job will have some pages at the lower, and some at the higher rate
    
    //The pages over the threshold are the number of pages so far this month, plus these pages MINUS the threshold
    monoPagesOver = (monoPrintsThisMonth + inputs.job.totalGrayscalePages) - thresholdMonoPrints;
    
    //The pages under then are the pages in this job, less the pages over
    var monoPagesUnder = inputs.job.totalGrayscalePages - monoPagesOver;
    
    //And the cost of the job is the combination of the over pages and the high rate, and the pages under and the low rate
    monoPagesJobCost = (monoPagesOver * highMonoCost) + (monoPagesUnder * lowMonoCost);
  }
  
  actions.log.debug("Charging "+monoPagesOver+"/"+inputs.job.totalGrayscalePages+" mono pages, "+colorPagesOver+"/"+inputs.job.totalColorPages+" color pages at high rates");
  actions.job.setCost(monoPagesJobCost + colorPagesJobCost);
  
  if (monoKeyExists) {
    actions.printer.onCompletionIncrementNumberProperty(myMonoKey, inputs.job.totalGrayscalePages, {'saveWhenCancelled' : false});
  } else {
    actions.printer.onCompletionSaveProperty(myMonoKey, inputs.job.totalGrayscalePages, {'saveWhenCancelled' : false});
  }
  
  if (colorKeyExists) {
    actions.printer.onCompletionIncrementNumberProperty(myColorKey, inputs.job.totalColorPages, {'saveWhenCancelled' : false});
  } else {
    actions.printer.onCompletionSaveProperty(myColorKey, inputs.job.totalColorPages, {'saveWhenCancelled' : false});
  }
  
  //Get the number of color and mono prints for this queue, for this month so far
  actions.log.info("Mono prints this month: " + (monoPrintsThisMonth + inputs.job.totalGrayscalePages) + " , Color prints this month: " + (colorPrintsThisMonth + inputs.job.totalColorPages));
}


