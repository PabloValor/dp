'use strict';
angular.module('app.games')

.factory('GameService', ['$http', 'SETTINGS', function($http, SETTINGS) {
    return {
        all: function(f_success, f_error) {
                $http.get(SETTINGS.url.games())
                    .success(function(response) {
                        console.log(response)

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
        new: function(game, f_success, f_error) {
                $http.post(SETTINGS.url.newGame(), game)
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
        },
        get: function(game_id, f_success, f_error) {
                $http.get(SETTINGS.url.game(game_id))
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
        },
        updateGamePlayerStatus : function(gameplayer_id, status, f_success, f_error) {
            $http.put(SETTINGS.url.gamePlayerStatus(gameplayer_id), { 'status': status })
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
        inviteFriends : function(game, friends, f_success, f_error) {
            var gamefriends = friends.map(function(f) { return {'player': f.id, 'game': game.id}; });
            console.log("invitando amigos");
            console.log(gamefriends);
            $http.post(SETTINGS.url.gamePlayerCreate(),  gamefriends)
                .success(function(response) {
                    console.log("respuesta");
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
