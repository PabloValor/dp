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
        },
        clearCache: function() {
            delete Data.allGames;
        }
    }
}])

.factory('TournamentService', ['$http', 'SETTINGS', 'Data', 
    function($http, SETTINGS, Data) {
    return {
        getAll: function(f_s, f_e) {
            if(!!Data.allTournaments) {
                f_s(Data.allTournaments);
                return;
            } 

            $http.get(SETTINGS.url.allTournaments())
                .success(function(response) {

                    Data.allTournaments = response;

                    console.info("All Tournaments")
                    console.info(response)                    
                    f_s(response);
                })
                .error(function(response) {
                    console.error("All Tournaments")
                    f_e(response);
                });
        },
        getAllWithTeams: function(f_s, f_e) {
            if(!!Data.allTournaments) {
                f_s(Data.allTournaments);
                return;
            } 

            $http.get(SETTINGS.url.allTournamentsTeams())
                .success(function(response) {

                    Data.allTournaments = response;

                    console.info("All Tournaments Teams")
                    console.info(response)
                    f_s(response);
                })
                .error(function(response) {
                    console.error("All Tournaments Teams")
                    f_e(response);
                });
        },                
        getAllTournamentsNextFixture: function(f_s, f_e) {
            if(!!Data.allTournamentsNextFixture) {
                f_s(Data.allTournamentsNextFixture);
                return;
            } 

            $http.get(SETTINGS.url.allTournamentsNextFixture())
                .success(function(response) {

                    Data.allTournamentsNextFixture = response;

                    console.info("Next Fixture")
                    f_s(response);
                })
                .error(function(response) {
                    console.error("Next Fixture")
                    console.error(response)
                    f_e(response)
                });
        },
        getAllTournamentsCurrentOrLastFixture: function(f_s, f_e) {
            if(!!Data.allTournamentsCurrentOrLastFixture) {
                f_s(Data.allTournamentsCurrentOrLastFixture);
                return;
            } 

            $http.get(SETTINGS.url.allTournamentsCurrentOrLastFixture())
                .success(function(response) {
                    
                    Data.allTournamentsCurrentOrLastFixture = response;

                    console.info("Current Fixture")
                    f_s(response);
                })
                .error(function(response) {
                    console.error("Current Fixture")
                    console.error(response)
                    f_e(response)
                });
        },
        getTournamentStats: function(tournament_id, f_s, f_e) {
            if(!!Data.tournamentStats && !!Data.tournamentStats[tournament_id]) {
                f_s(Data.tournamentStats[tournament_id]);
                return;
            } 

            $http.get(SETTINGS.url.tournamentStats(tournament_id))
                .success(function(response) {
                    if(!!!Data.tournamentStats) {
                        Data.tournamentStats = {};
                    } 

                    Data.tournamentStats[tournament_id] = response;

                    console.info("Current Fixture")
                    f_s(response);
                })
                .error(function(response) {
                    console.error("Current Fixture")
                    console.error(response)
                    f_e(response)
                });
        }
    }
}]);
