'use strict';
angular.module('app.users')

.controller('LoginController', ['$scope', '$location', '$http', 'AuthenticationService', 'Facebook', 'SETTINGS', '$rootScope',
    function($scope, $location, $http, AuthenticationService, Facebook, SETTINGS, $rootScope)  {
        if(AuthenticationService.isAuthenticated()) {
            $location.path('/');
        }

        $scope.credentials = {
            username: '',
            password: '' 
        };

        $scope.login = function() {
            //$rootScope.loadingInit = true;
            $scope.error = '';
            AuthenticationService.login($scope.credentials,
                function(response) {
                    $rootScope.loadingInit = false;
                    $rootScope.$broadcast("userLoginSuccess");
                    $location.path('/');

                }, function(response) {
                    $rootScope.loadingInit = false;
                    $scope.error = response.non_field_errors[0];
                });
        };

        $scope.login_fb = function() {
            //$rootScope.loadingInit = true;
            $scope.error = '';
            Facebook.login(
                function(response) { 
                    $rootScope.loadingInit = false;
                    $rootScope.$broadcast("userLoginSuccess");
                    $location.path('/');
                }, 
                function(response) { 
                    $rootScope.loadingInit = false;
                    $scope.error = response.non_field_errors[0];
                });
        };

        $scope.logout = function() {
            AuthenticationService.logout();
        };

    }
])

.controller('SignupController', ['$scope', '$location', 'UserService', 'AuthenticationService', 'Facebook',
    function($scope, $location, UserService, AuthenticationService, Facebook)  {
        if(AuthenticationService.isAuthenticated()) {
            $location.path('/');
        }

        $scope.user = {
            username: '',
            email: '',
            password: '' 
        };

        $scope.signup_fb = function() {
            Facebook.login(
                function(response) { 
                    $location.path('/');
                }, 
                function(response) { console.log(response); });
        };

        $scope.signup = function(user) {
            delete $scope.errors;
            UserService.create(user, 
                function(response) {
                    $location.path('/signin');
                },
                function(errors) {
                  $scope.errors = errors;
                  console.error(errors);
                });
        };
    }
]);
