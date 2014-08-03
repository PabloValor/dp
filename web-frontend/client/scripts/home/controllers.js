'use strict';
angular.module('app.home')

.controller('HeaderController', ['$scope', 'UserService', 
    function($scope, UserService)  {
        $scope.username = function() {
          return UserService.getUsername();
        };
    }
])
