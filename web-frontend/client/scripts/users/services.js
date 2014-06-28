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

.factory('UserService', ['$http', 'SETTINGS', function($http, SETTINGS) {
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
        }
    }
}])

.factory('Facebook',['$q', '$window', '$rootScope', 
    function($q, $window, $rootScope) {
	var resolve = function(errval, retval, deferred) {
          $rootScope.$apply(function() {
	        if (errval) {
		    deferred.reject(errval);
	        } else {
		    retval.connected = true;
	            deferred.resolve(retval);
	        }
	    });
        }

	var _login = function(){
	    var deferred = $q.defer();
            //first check if we already have logged in
	    FB.getLoginStatus(function(response) {
                console.log(response);
	        if (response.status === 'connected') {
	            // the user is logged in and has authenticated your
		    // app
		    console.log("fb user already logged in");
		    deferred.resolve(response);
		} else {
		    // the user is logged in to Facebook, 
		    // but has not authenticated your app
		    FB.login(function(response){
		        if(response.authResponse){
			    console.log("fb user logged in");
			    resolve(null, response, deferred);
			}else{
			    console.log("fb user could not log in");
			    resolve(response.error, null, deferred);
			}
		    });
		 }
	     });
			
	     return deferred.promise;
	}

	return{
		login: _login,
	};
}]);
