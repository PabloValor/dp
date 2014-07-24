'use strict';
angular.module('app.core')

.controller('HeaderController', ['$scope', 'UserService', 
    function($scope, UserService)  {
        $scope.username = UserService.getUsername();
    }
])
