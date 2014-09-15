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
            $rootScope.loadingLogin = true;
            $scope.error = '';
            AuthenticationService.login($scope.credentials,
                function(response) {
                    $rootScope.$broadcast("userLoginSuccess");
                    $location.path('/dashboard');

                }, function(response) {
                    $rootScope.loadingInit = false;
                    $scope.error = response.non_field_errors[0];
                });
        };

        $scope.login_fb = function() {
            $rootScope.loadingLogin = true;
            $scope.error = '';
            Facebook.login(
                function(response) { 
                    $rootScope.$broadcast("userLoginSuccess");
                    $location.path('/dashboard');
                }, 
                function(response) { 
                    $rootScope.loadingLogin = false;
                    $scope.error = response.non_field_errors[0];
                });
        };

        $scope.logout = function() {
            AuthenticationService.logout();
        };

    }
])

.controller('SignupController', ['$scope', '$location', 'UserService', 'AuthenticationService', 'Facebook', '$rootScope',
    function($scope, $location, UserService, AuthenticationService, Facebook, $rootScope)  {
        if(AuthenticationService.isAuthenticated()) {
            $location.path('/dashboard');
        }

        $scope.user = {
            username: '',
            email: '',
            password: '' 
        };

        $scope.signup_fb = function() {
            $rootScope.loadingLogin = true;
            Facebook.login(
                function(response) { 
                    $location.path('/dashboard');
                }, 
                function(response) { console.log(response); 
                                     $rootScope.loadingLogin = false; });

        };

        $scope.signup = function(user) {
            $rootScope.loadingLogin = true;
            delete $scope.errors;
            UserService.create(user, 
                function(response) {
                    $rootScope.loadingLogin = false;
                    $location.path('/signin');
                },
                function(errors) {
                  $rootScope.loadingLogin = false;
                  $scope.errors = errors;
                  console.error(errors);
                });
        };
    }
]);
