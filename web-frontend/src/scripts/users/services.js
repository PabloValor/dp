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
    };

    this.initUser = function(response) {
        console.info('Init User');
        console.info(response);
        this.create('token', response.token);
        this.create('username', response.username);
        this.create('user_id', response.user_id);
        this.create('friend_notifications', JSON.stringify(response.friend_notifications));
        this.create('game_notifications', JSON.stringify(response.game_notifications));
        this.create('games_count', JSON.stringify(response.games_count));
        this.create('games_points', JSON.stringify(response.games_points));
        this.create('friends_count', JSON.stringify(response.friends_count));        
    };

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

.factory('AuthenticationService', ['$http', 'Session', 'SETTINGS', 
    function($http, Session, SETTINGS, Data) {
        return {
            login: function(credentials, f_success, f_error) {
                return $http.post(SETTINGS.url.auth(), credentials)
                            .success(function(response) {

                                Session.initUser(response);                                
                                
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

                                Session.initUser(response);
                                
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

.factory('UserService', ['$http', 'SETTINGS', 'Session', 'Data',  
    function($http, SETTINGS, Session, Data) {
    return {
        getUsername : function(){
          return Session.get('username');
        },
        getUserID : function(){
          return Session.get('user_id');
        },
        getToken: function(){
          return Session.get('token');
        },
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
        search: function(username, f_success, f_error) {
            $http.get(SETTINGS.url.playerSearch(username))
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
        clearCache : function() {
            delete Data.search;
        }
    }
}])

.factory('Facebook',['$http',  '$window', '$rootScope', 'AuthenticationService', 'Session', 
    function($http, $window, $rootScope, AuthenticationService, Session) {
	return {
		login: function(f_success, f_error) {
                    FB.getLoginStatus(function(response) {
                        if (response.status === 'connected') {
                            console.log(response)
                            AuthenticationService.login_social(response.authResponse.accessToken, "facebook", f_success, f_error);
                        } else {
                            FB.login(function(response) {
                                console.log(response)
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
