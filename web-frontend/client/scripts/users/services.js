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

.factory('AuthenticationService', ['$http', 'Session', function($http, Session) {
        return {
            login: function(credentials, f_success, f_error) {
                console.log(credentials);
                return $http.post('http://127.0.0.1:8000/api-token-auth/', credentials)
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
                console.log(Session.get('token'));
                return !!Session.get('token');
            }
        };
    }
])

.factory('TokenInterceptor', ['$q', 'Session', function($q, Session) {
    return {
        request: function(config) {
            config.headers = config.headers || {};
            if(!!Session.get('token')) {
                config.headers['WWW-Authenticate'] = Session.get('token');
            }

            return config;
        },
        response: function(response) {
            return response || $q.when(response);
        }
    };
}]);
