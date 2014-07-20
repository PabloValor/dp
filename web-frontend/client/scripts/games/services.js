'use strict';
angular.module('app.games')

.factory('GameService', ['$http', function($http) {
    return {
        all: function(f_success, f_error) {
                $http.get('http://127.0.0.1:8000/games/')
                    .success(function(response) {
                        console.log(response)
                    })
                    .error(function(response) {
                        console.log(response);

                        if(!!f_error) {
                            f_success(response);
                        }
                    });
            },
        new: function(game, f_success, f_error) {
                $http.post('http://127.0.0.1:8000/games/', game)
                    .success(function(response) {
                        console.log(response)

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

.factory('TournamentService', ['$http', function($http) {
    return {
        all: function(f_success, f_error) {
                $http.get('http://127.0.0.1:8000/tournaments/')
                    .success(function(response) {
                        console.log(response)

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
}]);
