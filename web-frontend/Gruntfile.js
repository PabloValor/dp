'use strict';

var path = require('path');


module.exports = function(grunt) {

    // Project configuration.
    grunt.initConfig({
        express: {
            livereload: {
                options: {
                    port: 9090,
                    bases: path.resolve('src'),
                    monitor: {},
                    debug: true,
                    server: path.resolve('./app/server')
                }
            }
        },

        compass: {
            dev: {
                options: {
                    sassDir: 'src/sass',
                    imagesDir: "src/sass/ui/images/",
                    javascriptsDir: "src/scripts",
                    fontsDir: "src/fonts",
                    httpFontsPath: "fonts",
                    importPath: "src/bower_components",
                    httpGeneratedImagesPath: "src/sass/ui/images/",
                    cssDir: 'src/css',
                    relativeAssets: true,
                    environment: 'development'
                }
            },
            build: {
                options: {
                    sassDir: '.tmp/sass',
                    imagesDir: ".tmp/sass/ui/images/",
                    javascriptsDir: ".tmp/scripts",
                    fontsDir: ".tmp/fonts",
                    httpFontsPath: "fonts",
                    importPath: "src/bower_components",
                    httpGeneratedImagesPath: ".tmp/sass/ui/images/",
                    cssDir: '.tmp/css',
                    relativeAssets: true,
                    environment: 'production'
                }
            }            
        },

        regarde: {
            pub: {
                files: 'src/**/*',
                tasks: ['livereload']
            },
            trigger: {
                files: '.server',
                tasks: 'express-restart:livereload'
            },
            sass: {
                files: 'src/sass/**/*.scss',
                tasks: ['format']
            }            
        },
        
        uglify: {
            options: {
                mangle: false
            },
            build: {
                files: {
                    '.tmp/js/site.js': ['.tmp/js/site.js']
                }
            }            
        },
        
        clean: {
            'pre-build': ['.tmp', 'public'],
            'post-build': ['.tmp']            
        },
        
        copy: {
            'pre-build': {
                files: [
                    { expand: true,
                      cwd: 'src/',
                      src: ['index.html','404.html','favicon.ico',
                            'sass/**',
                            'scripts/**',
                            'fonts/**',
                            'i18n/**',                           
                            'images/**',                            
                            'views/**'],                      
                      dest: '.tmp/' }
                ]
            },
            'bower-css': {
                files: [
                    { expand: true,
                      cwd: 'src/',
                      src: ['bower_components/font-awesome/**', // The CSS is need it
                            'bower_components/morris.js/**',
                            'css/bootstrap/**',
                            'css/img/**'],
                      dest: 'public/' }
                ]
            },
            'post-build': {
                files: [
                    {expand: true,
                     cwd: '.tmp/',
                     src:['index.html','404.html','favicon.ico',
                          'css/**',
                          'js/**',
                          'fonts/**',
                          'i18n/**',                           
                          'images/**',
                          'scripts/**/views/*',
                          'views/**',
                         ],
                     dest: 'public/' }
                ]
            }            
        },
        usemin: {
            html: '.tmp/index.html'
        },

        concat: {
            options: {
                stripBanners: true,
                separator: '\n;'
            },
            'build-vendor': {
                src: ["src/bower_components/jquery/dist/jquery.min.js",
                      "src/bower_components/angular/angular.min.js",
                      "src/bower_components/angular-route/angular-route.min.js",
                      "src/bower_components/angular-animate/angular-animate.min.js",
                      "src/bower_components/underscore/underscore-min.js",

                      'src/bower_components/angular-socket-io/socket.js',
                      "src/bower_components/angular-bootstrap/ui-bootstrap-tpls.min.js",
                      "src/bower_components/jquery-spinner/dist/jquery.spinner.min.js",
                      "src/bower_components/seiyria-bootstrap-slider/dist/bootstrap-slider.min.js",
                      "src/bower_components/toastr/toastr.min.js",
                      "src/bower_components/bootstrap-file-input/bootstrap.file-input.js",
                      "src/bower_components/jquery.slimscroll/jquery.slimscroll.min.js",
                      "src/bower_components/holderjs/holder.js",
                      "src/bower_components/raphael/raphael-min.js",
                      "src/bower_components/morris.js/morris.js",
                      "src/bower_components/flot/jquery.flot.js",
                      "src/bower_components/flot/jquery.flot.resize.js",
                      "src/bower_components/flot/jquery.flot.pie.js",
                      "src/bower_components/flot/jquery.flot.stack.js",
                      "src/bower_components/flot.tooltip/js/jquery.flot.tooltip.min.js",
                      "src/bower_components/flot/jquery.flot.time.js",
                      "src/bower_components/gauge.js/dist/gauge.min.js",
                      "src/bower_components/jquery.easy-pie-chart/dist/angular.easypiechart.min.js",
                      "src/bower_components/angular-wizard/dist/angular-wizard.min.js",
                      "src/bower_components/textAngular/dist/textAngular-sanitize.min.js",
                      "src/bower_components/textAngular/dist/textAngular.min.js",
                      "src/bower_components/chartjs/Chart.js",
                      "src/vendors/*.js"
                     ],
                dest: '.tmp/js/vendor.js',
            },
            'build-src': {
                src: ["src/scripts/app.js",
                      'src/scripts/shared/main.js',
                      'src/scripts/**/*.js'
                     ],                
                dest: '.tmp/js/site.js',
            }
        },
        'string-replace': {
            build: {
                files: {
                    '.tmp/js/site.js': '.tmp/js/site.js' 
                },
                options:{
                    replacements: [
                        { 
                            pattern: '127.0.0.1:8000',
                            replacement: 'api.dpfutbol.com'
                        }
                    ]
                }
            }
        }        

    });

    // These plugins provide necessary tasks.
    grunt.loadNpmTasks('grunt-contrib-compass');
    grunt.loadNpmTasks('grunt-contrib-livereload');
    grunt.loadNpmTasks('grunt-contrib-copy');
    grunt.loadNpmTasks('grunt-contrib-clean');
    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-string-replace');    
    grunt.loadNpmTasks('grunt-express');
    grunt.loadNpmTasks('grunt-regarde');
    grunt.loadNpmTasks('grunt-usemin');    


    grunt.registerTask('format', ['compass:dev']);
    grunt.registerTask('server', ['livereload-start', 'express', 'regarde']);

    grunt.registerTask('clean-build', ['clean:before-build']);
    grunt.registerTask('build', ['clean:pre-build',
                                 'copy:pre-build',
                                 'compass:build',
                                 'concat:build-vendor',
                                 'concat:build-src',
                                 'string-replace:build',
                                 'uglify',
                                 'usemin',
                                 'copy:post-build',
                                 'copy:bower-css',
                                 'clean:post-build'
                                 ]);
    
    grunt.registerTask('nico', ['concat']);    
    grunt.registerTask('default', ['format', 'server']);

};
