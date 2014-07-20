'use strict';
angular.module('app.users')

.service('Session', ['$window', function($window) {
    this.create = function(key, value) {
        $window.sessionStorage[key] = value;
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
                return $http.post(SETTINGS.url.auth(), credentials)
                            .success(function(response) {
                                console.log(response)
                                Session.create('token', response.token);
                                Session.create('id', response.id);
                                if(!!f_success) {
                                    f_success(response);
                                }
                            })
                            .error(function(response) {
                                console.log(response);

                                if(!!f_error) {
                                    f_error(response);
                                }
                            });
            },
            login_social: function(token, backend, f_success, f_error) {
                Session.create('fb-token', token);

                return $http.post(SETTINGS.url.social_auth(backend), 
                                  { "access_token": token, "backend": backend })

                            .success(function(response) {
                                        Session.create('token', response.token);

                                        if(!!f_success) {
                                            f_success(response);
                                        }
                            })
                            .error(function(response) {
                                console.log(response);

                                if(!!f_error) {
                                    f_error(response);
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

.factory('UserService', ['$http', 'SETTINGS', 'Session',  function($http, SETTINGS, Session) {
    return {
        create: function(user, f_success, f_error) {
            $http.post(SETTINGS.url.player(), user)
                .success(function(response) {
                    console.log(response);

                    if(!!f_success) {
                        f_success(response);
                    }
                })
                .error(function(response) {
                    console.log(response);

                    if(!!f_error) {
                        f_error(response);
                    }
                });
        }, 
        getFriends: function(f_success, f_error) {
            $http.get(SETTINGS.url.playerFriends(Session.get('id')))
                .success(function(response) {
                    console.log(response);

                    if(!!f_success) {
                        f_success(response);
                    }
                })
                .error(function(response) {
                    console.log(response);

                    if(!!f_error) {
                        f_error(response);
                    }
                });
            }
        }
}])

.factory('Facebook',['$http',  '$window', '$rootScope', 'AuthenticationService', 'Session', 
    function($http, $window, $rootScope, AuthenticationService, Session) {
	return {
		login: function(f_success, f_error) {
                    FB.getLoginStatus(function(response) {
                        if (response.status === 'connected') {
                            AuthenticationService.login_social(response.authResponse.accessToken, "facebook", f_success, f_error);
                        } else {
                            FB.login(function(response) {
                                if(response.authResponse) {
                                    AuthenticationService.login_social(response.authResponse.accessToken, "facebook", f_success, f_error);
                                } else {
                                    console.log('impossible to connect');
                                }
                            }, { scope: ['public_profile', 'email', 'user_friends']});
                        }
                    });
                }, 
                getFriends: function(f_success, f_error) {
                    $http.get("https://graph.facebook.com/v2.0/me/invitable_friends", { params: {'access_token': Session.get('fb-token')}})
                        .success(function (response) {
                                    console.log(response);
                                    if (response && !response.error) {
                                        if(!!f_success) {
                                            f_success(response);
                                        }
                                    }

                                })
                        .error(function (response) {
                                    if(!!f_error) {
                                        f_error(response);
                                    }
                                })
                },
                isAuthenticated: function() {
                    return !!Session.get('fb-token');
                }
	};
}]);
