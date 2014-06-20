// Karma configuration
// Generated on Fri Jun 20 2014 15:52:17 GMT-0300 (ART)

module.exports = function(config) {
  config.set({

    // base path that will be used to resolve all patterns (eg. files, exclude)
    basePath: 'client',


    // frameworks to use
    // available frameworks: https://npmjs.org/browse/keyword/karma-adapter
    frameworks: ['jasmine'],


    // list of files / patterns to load in the browser
    files: [
      'bower_components/jquery/dist/jquery.min.js',
      'bower_components/angular/angular.min.js',
      'bower_components/angular-route/angular-route.min.js',
      'bower_components/angular-animate/angular-animate.min.js',
      'bower_components/underscore/underscore-min.js',
      'bower_components/angular-mocks/angular-mocks.js',

      'bower_components/jquery.easy-pie-chart/dist/angular.easypiechart.min.js',
      'bower_components/angular-bootstrap/ui-bootstrap-tpls.min.js',
      'bower_components/jquery-spinner/dist/jquery.spinner.min.js',
      'bower_components/seiyria-bootstrap-slider/dist/bootstrap-slider.min.js',
      'bower_components/jquery-steps/build/jquery.steps.min.js',
      'bower_components/toastr/toastr.min.js',
      'bower_components/bootstrap-file-input/bootstrap.file-input.js',
      'bower_components/jquery.slimscroll/jquery.slimscroll.min.js',
      'bower_components/holderjs/holder.js',
      'bower_components/raphael/raphael-min.js',
      'bower_components/morris.js/morris.js',
      'scripts/vendors/responsive-tables.js',
      'scripts/vendors/jquery.sparkline.min.js',
      'bower_components/flot/jquery.flot.js',
      'bower_components/flot/jquery.flot.resize.js',
      'bower_components/flot/jquery.flot.pie.js',
      'bower_components/flot/jquery.flot.stack.js',
      'bower_components/flot.tooltip/js/jquery.flot.tooltip.min.js',
      'bower_components/flot/jquery.flot.time.js',
      'bower_components/gauge.js/dist/gauge.min.js',
      'bower_components/jquery.easy-pie-chart/dist/angular.easypiechart.min.js',
      'bower_components/angular-wizard/dist/angular-wizard.min.js',
      'bower_components/textAngular/dist/textAngular-sanitize.min.js',
      'bower_components/textAngular/dist/textAngular.min.js',

      'scripts/app.js',
      'scripts/**/*.js'
    ],


    // list of files to exclude
    exclude: [
      
    ],


    // preprocess matching files before serving them to the browser
    // available preprocessors: https://npmjs.org/browse/keyword/karma-preprocessor
    preprocessors: {
    
    },


    // test results reporter to use
    // possible values: 'dots', 'progress'
    // available reporters: https://npmjs.org/browse/keyword/karma-reporter
    reporters: ['progress'],


    // web server port
    port: 9876,


    // enable / disable colors in the output (reporters and logs)
    colors: true,


    // level of logging
    // possible values: config.LOG_DISABLE || config.LOG_ERROR || config.LOG_WARN || config.LOG_INFO || config.LOG_DEBUG
    logLevel: config.LOG_INFO,


    // enable / disable watching file and executing tests whenever any file changes
    autoWatch: true,


    // start these browsers
    // available browser launchers: https://npmjs.org/browse/keyword/karma-launcher
    browsers: ['Chrome'],


    // Continuous Integration mode
    // if true, Karma captures browsers, runs the tests and exits
    singleRun: false
  });
};
