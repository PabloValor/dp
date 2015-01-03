'use strict';
angular.module('app.games')

.factory('GameService', ['$http', 'SETTINGS', 'NotificationService', 
    function($http, SETTINGS, NotificationService) {
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
                            f_error(response);
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
        updateGamePlayerAnotherChance : function(gameplayer_id, another_chance, f_success, f_error) {
            $http.put(SETTINGS.url.gamePlayerAnotherChance(gameplayer_id), { 'another_chance': another_chance })
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
        updateGamePlayerInvitePlayerAgain : function(gameplayer_id, f_success, f_error) {
            $http.put(SETTINGS.url.gamePlayerInviteAgain(gameplayer_id))
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
            var gamefriends = friends.map(function(f) { return {'player': f.id, 'game': game.id, 'initial_points': f.initial_points }; });
            $http.post(SETTINGS.url.gamePlayerCreate(),  gamefriends)
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
        getGameNotification : function(game_id) {
          var game_notifications = NotificationService.getGameNotifications();
          var game_notification;

          for(var i in game_notifications) {
            game_notification = game_notifications[i];
            if(game_notification.game_id == game_id) {
              return game_notification;
            }
          }

          return null;
        }
    }
}])

.factory('TournamentService', ['$http', 'SETTINGS', function($http, SETTINGS) {
    return {
        getAll: function(f_s, f_e) {
            return $http.get(SETTINGS.url.allTournaments())
                .success(function(response) {
                    f_s(response);
                })
                .error(function(response) {
                    console.error("errror")
                    f_e(response);
                });
        },        
        getAllTournamentsNextFixture: function(f) {
            return $http.get(SETTINGS.url.allTournamentsNextFixture())
                .success(function(response) {
                    f(response);
                })
                .error(function(response) {
                    f(response);
                });
        },
        getAllTournamentsCurrentOrLastFixture: function(f) {
            return $http.get(SETTINGS.url.allTournamentsCurrentOrLastFixture())
                .success(function(response) {
                    f(response);
                })
                .error(function(response) {
                    f(response);
                });
        }                
    }
}]);
