'use strict';
angular.module('app.users')

.controller('LoginController', ['$scope', '$location', 'AuthenticationService', 
    function($scope, $location, AuthenticationService)  {

        if(AuthenticationService.isAuthenticated()) {
            $location.path('/');
        }

        $scope.credentials = {
            username: '',
            password: '' 
        };

        $scope.login = function() {
            AuthenticationService.login($scope.credentials);
        };

        $scope.logout = function() {
            AuthenticationService.logout();
        };
    }
]);


