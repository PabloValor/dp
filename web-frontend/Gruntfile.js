(function() {
  "use strict";
  var LIVERELOAD_PORT, lrSnippet, mountFolder;

  LIVERELOAD_PORT = 35728;

  lrSnippet = require("connect-livereload")({
    port: LIVERELOAD_PORT
  });

  mountFolder = function(connect, dir) {
    return connect["static"](require("path").resolve(dir));
  };

  module.exports = function(grunt) {
    var yeomanConfig;
    require("load-grunt-tasks")(grunt);
    require("time-grunt")(grunt);
    yeomanConfig = {
      app: "client",
      dist: "dist"
    };
    try {
      yeomanConfig.app = require("./bower.json").appPath || yeomanConfig.app;
    } catch (_error) {}
    grunt.initConfig({
      yeoman: yeomanConfig,
      watch: {
        compass: {
          files: ["<%= yeoman.app %>/styles/**/*.{scss,sass}"],
          tasks: ["compass:server"]
        },
        livereload: {
          options: {
            livereload: LIVERELOAD_PORT
          },
          files: ["<%= yeoman.app %>/index.html", "<%= yeoman.app %>/views/**/*.html", "<%= yeoman.app %>/styles/**/*.scss", ".tmp/styles/**/*.css", "{.tmp,<%= yeoman.app %>}/scripts/**/*.js", "<%= yeoman.app %>/images/**/*.{png,jpg,jpeg,gif,webp,svg}"]
        }
      },
      connect: {
        options: {
          port: 3000,
          hostname: "localhost"
        },
        livereload: {
          options: {
            middleware: function(connect) {
              return [lrSnippet, mountFolder(connect, ".tmp"), mountFolder(connect, yeomanConfig.app)];
            }
          }
        },
        test: {
          options: {
            middleware: function(connect) {
              return [mountFolder(connect, ".tmp"), mountFolder(connect, "test")];
            }
          }
        },
        dist: {
          options: {
            middleware: function(connect) {
              return [mountFolder(connect, yeomanConfig.dist)];
            }
          }
        }
      },
      open: {
        server: {
          url: "http://localhost:<%= connect.options.port %>"
        }
      },
      clean: {
        dist: {
          files: [
            {
              dot: true,
              src: [".tmp", "<%= yeoman.dist %>/*", "!<%= yeoman.dist %>/.git*"]
            }
          ]
        },
        server: ".tmp"
      },
      jshint: {
        options: {
          jshintrc: ".jshintrc"
        },
        all: ["Gruntfile.js", "<%= yeoman.app %>/scripts/**/*.js"]
      },
      compass: {
        options: {
          sassDir: "<%= yeoman.app %>/styles",
          cssDir: ".tmp/styles",
          generatedImagesDir: ".tmp/styles/ui/images/",
          imagesDir: "<%= yeoman.app %>/styles/ui/images/",
          javascriptsDir: "<%= yeoman.app %>/scripts",
          fontsDir: "<%= yeoman.app %>/fonts",
          importPath: "<%= yeoman.app %>/bower_components",
          httpImagesPath: "styles/ui/images/",
          httpGeneratedImagesPath: "styles/ui/images/",
          httpFontsPath: "fonts",
          relativeAssets: true
        },
        dist: {
          options: {
            debugInfo: false,
            noLineComments: true
          }
        },
        server: {
          options: {
            debugInfo: true
          }
        },
        forvalidation: {
          options: {
            debugInfo: false,
            noLineComments: false
          }
        }
      },
      useminPrepare: {
        html: "<%= yeoman.app %>/index.html",
        options: {
          dest: "<%= yeoman.dist %>",
          flow: {
            steps: {
              js: ["concat"],
              css: ["concat"]
            },
            post: []
          }
        }
      },
      usemin: {
        html: ["<%= yeoman.dist %>/**/*.html", "!<%= yeoman.dist %>/bower_components/**"],
        css: ["<%= yeoman.dist %>/styles/**/*.css"],
        options: {
          dirs: ["<%= yeoman.dist %>"]
        }
      },
      htmlmin: {
        dist: {
          options: {},
          files: [
            {
              expand: true,
              cwd: "<%= yeoman.app %>",
              src: ["*.html", "views/*.html"],
              dest: "<%= yeoman.dist %>"
            }
          ]
        }
      },
      copy: {
        dist: {
          files: [
            {
              expand: true,
              dot: true,
              cwd: "<%= yeoman.app %>",
              dest: "<%= yeoman.dist %>",
              src: ["favicon.ico", "bower_components/font-awesome/css/*", "bower_components/font-awesome/fonts/*", "bower_components/weather-icons/css/*", "bower_components/weather-icons/font/*", "fonts/**/*", "i18n/**/*", "images/**/*", "styles/bootstrap/**/*", "styles/fonts/**/*", "styles/img/**/*", "styles/ui/images/**/*", "views/**/*"]
            }, {
              expand: true,
              cwd: ".tmp",
              dest: "<%= yeoman.dist %>",
              src: ["styles/**", "assets/**"]
            }, {
              expand: true,
              cwd: ".tmp/images",
              dest: "<%= yeoman.dist %>/images",
              src: ["generated/*"]
            }, {
              expand: true,
              cwd: "<%= yeoman.app %>/scripts",
              src: "**/*.js",
              dest: ".tmp/scripts",
              ext: ".js"
            }
          ]
        },
        styles: {
          expand: true,
          cwd: "<%= yeoman.app %>/styles",
          dest: ".tmp/styles/",
          src: "**/*.css"
        }
      },
      concurrent: {
        server: ["compass:server", "copy:styles"],
        dist: ["compass:dist", "copy:styles", "htmlmin"]
      },
      concat: {
        options: {
          separator: grunt.util.linefeed + ';' + grunt.util.linefeed
        },
        dist: {
          src: ["<%= yeoman.dist %>/bower_components/angular/angular.min.js"],
          dest: "<%= yeoman.dist %>/scripts/vendor.js"
        }
      },
      uglify: {
        options: {
          mangle: false
        },
        dist: {
          files: {
            "<%= yeoman.dist %>/scripts/app.js": [".tmp/**/*.js"]
          }
        }
      }
    });
    grunt.registerTask("server", function(target) {
      if (target === "dist") {
        return grunt.task.run(["build", "open", "connect:dist:keepalive"]);
      }
      return grunt.task.run(["clean:server", "concurrent:server", "connect:livereload", "open", "watch"]);
    });
    grunt.registerTask("build", ["clean:dist", "useminPrepare", "concurrent:dist", "copy:dist", "concat", "uglify", "usemin"]);
    return grunt.registerTask("default", ["server"]);
  };

}).call(this);
