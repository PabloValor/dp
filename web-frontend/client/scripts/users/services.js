'use strict';
angular.module('app.users')

.factory('AuthenticationService', ['$http', function($http) {
        return {
            login: function(username, password) {
                $http.post('http://127.0.0.1:8000/api-token-auth/',
                    { username: username, password: password })
                    .success(function(response) { 
                        console.log(response) 
                    })
                    .error(function(response) { 
                        console.log(response) 
                    })
           }
        };
    }
]);
