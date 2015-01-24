'use strict';

var path = require('path');


module.exports = function(grunt) {

    // Project configuration.
    grunt.initConfig({
        express: {
            livereload: {
                options: {
                    port: 9090,
                    bases: path.resolve('public'),
                    monitor: {},
                    debug: true,
                    server: path.resolve('./app/server')
                }
            }
        },

        compass: {
            dev: {
                options: {
                    sassDir: 'public/sass',
                    imagesDir: "public/sass/ui/images/",
                    javascriptsDir: "public/scripts",
                    fontsDir: "public/fonts",
                    httpFontsPath: "fonts",
                    importPath: "public/bower_components",
                    httpGeneratedImagesPath: "public/sass/ui/images/",
                    cssDir: 'public/css',
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
                    importPath: ".tmp/bower_components",
                    httpGeneratedImagesPath: ".tmp/sass/ui/images/",
                    cssDir: '.tmp/css',
                    relativeAssets: true,
                    environment: 'production'
                }
            }            
        },

        regarde: {
            pub: {
                files: 'public/**/*',
                tasks: ['livereload']
            },
            trigger: {
                files: '.server',
                tasks: 'express-restart:livereload'
            },
            express: {
                files: 'app/templates/hello.dust',
                tasks: 'livereload'
            }
        },
        
        uglify: {
            options: {
                mangle: false
            },
            build: {
                files: {
                    '.tmp/js/site.min.js':
                    ['.tmp/scripts/app.js', '.tmp/scripts/shared/main.js', '.tmp/scripts/**/*.js', '.tmp/vendors/*.js']
                }
            }            
        },
        
        clean: {
            'before-build': ['.tmp', 'public'],
            'after-build': ['.tmp']            
        },
        
        copy: {
            'pre-build': {
                files: [
                    { expand: true, cwd: 'src/', src: '**', dest: '.tmp/' }
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
                          'views/**'], dest: 'public/' }
                ]
            }            
        },
        #
        useminPrepare: {
            html: '.tmp/index.html'
        }
    });

    // These plugins provide necessary tasks.
    grunt.loadNpmTasks('grunt-contrib-compass');
    grunt.loadNpmTasks('grunt-contrib-livereload');
    grunt.loadNpmTasks('grunt-contrib-copy');
    grunt.loadNpmTasks('grunt-contrib-clean');
    grunt.loadNpmTasks('grunt-usemin');    
    grunt.loadNpmTasks('grunt-express');
    grunt.loadNpmTasks('grunt-regarde');


    grunt.registerTask('format', ['compass:dev']);
    grunt.registerTask('server', ['livereload-start', 'express', 'regarde']);

    grunt.registerTask('clean-build', ['clean:before-build']);
    grunt.registerTask('build', ['clean:before-build',
                                 'useminPrepare',
                                 'concat:generated',
                                 'uglify:generated',
                                 'copy:pre-build',
                                 'compass:build',
                                 'usemin',
                                 'copy:post-build',
                                 'clean:after-build']);
    
    grunt.registerTask('default', ['format', 'server']);

};
