'use strict';
angular.module('app.core')

.controller('HeaderController', ['$scope', 'socket', 'UserService', 
    function($scope, socket, UserService)  {
      socket.on('message', function (message) {
        console.info('desde servidor');
        console.info(message);
      });
    }
])
