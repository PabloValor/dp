'use strict';
angular.module('app.users')

.controller('LoginController', ['$scope', '$location', '$http', 'AuthenticationService', 'Facebook', 'SETTINGS', '$rootScope',
    function($scope, $location, $http, AuthenticationService, Facebook, SETTINGS, $rootScope)  {
        if(AuthenticationService.isAuthenticated()) {
            $location.path('/noticias');
        }

        $scope.credentials = {
            username: '',
            password: '' 
        };

        $rootScope.loadingLogin = false;

        $scope.login = function() {
            $rootScope.loadingLogin = true;
            $scope.error = '';
            AuthenticationService.login($scope.credentials,
                function(response) {
                    $rootScope.$broadcast("userLoginSuccess");
                    $location.path('/noticias');

                }, function(response) {
                    $rootScope.loadingLogin = false;
                    $scope.error = response.non_field_errors[0];
                });
        };

        $scope.login_fb = function() {
            $rootScope.loadingLogin = true;
            $scope.error = '';
            Facebook.login(
                function(response) { 
                    $rootScope.$broadcast("userLoginSuccess");
                    $location.path('/noticias');
                }, 
                function(response) { 
                    $rootScope.loadingLogin = false;
                    $scope.error = response.non_field_errors[0];
                });
        };

        $scope.businessSiteSite = !!$rootScope.businessSite;

        if ($rootScope.businessSite) {
            $scope.placeholders =
                {
                    'username': 'nombre y apellido',
                    'password': 'clave'
                };
        } else {
            $scope.placeholders =
                {
                    'username': 'apodo',
                    'password': 'clave'
                };
        }        
    }
])

.controller('SignupController', ['$scope', '$location', 'UserService', 'AuthenticationService', 'Facebook', '$rootScope',
    function($scope, $location, UserService, AuthenticationService, Facebook, $rootScope)  {
        if(AuthenticationService.isAuthenticated()) {
            $location.path('/noticias');
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
                    $rootScope.$broadcast("userLoginSuccess");
                    $location.path('/noticias');
                }, 
                function(response) { console.log(response); 
                                     $rootScope.loadingLogin = false; });

        };

        $scope.signup = function(user) {
            $rootScope.loadingLogin = true;
            delete $scope.errors;
            UserService.create(user, 
                function(response) {
                    $location.path('/signin');
                },
                function(errors) {
                  $rootScope.loadingLogin = false;
                  $scope.errors = errors;
                  console.error(errors);
                });
        };

        if ($rootScope.businessSite) {
            $scope.placeholders =
                {
                    'username': 'nombre y apellido',
                    'password': 'clave',
                    'email': 'email corporativo'
                };
        } else {
            $scope.placeholders =
                {
                    'username': 'apodo',
                    'password': 'clave',
                    'email': 'email'
                };
        }

    }
]);
