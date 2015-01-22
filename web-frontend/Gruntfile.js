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
            dist: {
                files: {
                    'public/scripts/site.min.js':
                    ['public/scripts/app.js', 'public/scripts/shared/main.js', 'public/scripts/**/*.js', 'public/vendors/*.js']
                }
            }
        }
    });

    // These plugins provide necessary tasks.
    grunt.loadNpmTasks('grunt-contrib-compass');
    grunt.loadNpmTasks('grunt-contrib-livereload');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-express');
    grunt.loadNpmTasks('grunt-regarde');

    grunt.registerTask('format', ['compass', 'uglify']);
    grunt.registerTask('server', ['livereload-start', 'express', 'regarde']);
    // Default task.
    grunt.registerTask('default', ['format', 'server']);

};
