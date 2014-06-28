'use strict';
angular.module('app.users')

.controller('LoginController', ['$scope', '$location', '$http', 'AuthenticationService', 'Facebook', 'SETTINGS',
    function($scope, $location, $http, AuthenticationService, Facebook, SETTINGS)  {
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

        $scope.login_fb = function() {
            Facebook.login().then(function(response) {
                console.log("posteando");
                $http.post(SETTINGS.url.social_auth(), 
                    { "access_token": response.authResponse.accessToken, 
                      "backend": "facebook" })
                    .success(function(response) {
                        console.log(response);
                    })
                    .error(function(response) {
                        console.log(response);
                    });
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
