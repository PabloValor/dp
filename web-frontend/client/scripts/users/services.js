'use strict';
angular.module('app.users')

.service('Session', ['$window', function($window) {
    this.create = function(token) {
        $window.sessionStorage.token = token;
    };

    this.destroy = function() {
        delete $window.sessionStorage.token;
    };

    this.get = function(key) {
        return $window.sessionStorage[key];
    }

    return this;
}])

.factory('TokenInterceptor', ['$q', 'Session', function($q, Session) {
    return {
        request: function(config) {
            config.headers = config.headers || {};
            if(!!Session.get('token')) {
                config.headers['Authorization'] = 'Token ' + Session.get('token');
            }

            return config;
        },
        response: function(response) {
            return response || $q.when(response);
        }
    };
}])

.factory('AuthenticationService', ['$http', 'Session', 'SETTINGS', function($http, Session, SETTINGS) {
        return {
            login: function(credentials, f_success, f_error) {
                console.log(SETTINGS);
                return $http.post(SETTINGS.url.auth(), credentials)
                            .success(function(response) {
                                console.log(response)
                                Session.create(response.token);
                                if(!!f_success) {
                                    f_success(response);
                                }
                            })
                            .error(function(response) {
                                console.log(response);

                                if(!!f_error) {
                                    f_success(response);
                                }
                            });
            },
            logout: function() {
                Session.destroy();
            },
            isAuthenticated: function() {
                return !!Session.get('token');
            }
        };
    }
])

.factory('UserService', ['$http', 'SETTINGS', function($http, SETTINGS) {
    return {
        create: function(user) {
            $http.post(SETTINGS.url.player(), user)
                .success(function(response) {
                    console.log(response);
                })
                .error(function(response) {
                    console.log(response);
                });
        }
    }
}]);
