/* Project specific Javascript goes here. */

// Set the year for Copyright section
'#year'.html(function() {
  var today = new Date();
  var year = today.getFullYear();
  return year.toString();
});
