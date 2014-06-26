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
            AuthenticationService.login($scope.credentials,
                function(response) {
                    $location.path('/');
                });
        };

        $scope.logout = function() {
            AuthenticationService.logout();
        };

    }
])

.controller('SignupController', ['$scope', '$location', 'UserService', 'AuthenticationService',
    function($scope, $location, UserService, AuthenticationService)  {
        if(AuthenticationService.isAuthenticated()) {
            $location.path('/');
        }

        $scope.user = {
            username: '',
            email: '',
            password: '' 
        };

        $scope.signup = function(user) {
            $scope.signupFailed = {};
            UserService.create(user, 
                function(response) {
                    $location.path('/signin');
                },
                function(errors) {
                    // See different kinds of errors
                    $scope.signupFailed = { errors : errors };
                });
        };
    }
]);
