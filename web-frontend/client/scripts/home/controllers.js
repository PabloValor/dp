'use strict';
angular.module('app.home')

.controller('HeaderController', ['$scope', 'UserService', 
    function($scope, UserService)  {
        console.log("chau");
        $scope.username = UserService.getUsername();
        console.log($scope.username);
    }
])
