'use strict';
angular.module('app.users')

.controller('LoginController', ['$scope', 'AuthenticationService', function($scope, AuthenticationService) {
    $scope.login = function() {
        AuthenticationService.login($scope.username, $scope.password);
    }
}]);


