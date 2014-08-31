'use strict';
angular.module('app.games')

.controller('GameController', ['$scope', '$location', 'GameService', 'Data', 'UserService', '$rootScope',
    function($scope, $location, GameService, Data, UserService, $rootScope)  {
        $rootScope.loadingInit = true;
        GameService.all(function(games) {
          $scope.games = games.filter(function(game) { return !( game.you[0].status == false && game.you[0].another_chance == false) });

          $rootScope.loadingInit = false;
          if($scope.games.length == 1) {
            $scope.gameDetail($scope.games[0]);
          }
        }, function(response) {
          console.error(response);
          $rootScope.loadingInit = false;
        });

        $scope.gameDetail = function(game) {
          Data.currentGame = game;
          $location.path('/torneos/detalle/' + game.id);
        }

        $scope.username = UserService.getUsername();

        $scope.youGameStatus = "";
        $scope.gameSelectFilter = function(value) {
          var filter = $scope.youGameStatus;
          var status = value.you[0].status;
          var another_chance = value.you[0].another_chance;

          return (filter == "playing" && status ) ||
                 (filter == "waiting" && status == undefined) ||
                 (filter == "invitation" && status == false && another_chance) ||
                 (filter == "rejected" && status == false && !another_chance) ||
                 (filter == "");
        };
    }
])

.controller('NewGameController', ['$scope', '$location', 'TournamentService', 'GameService', 'Facebook', 'UserService', 'Data', 'FriendsService',
    function($scope, $location, TournamentService, GameService, Facebook, UserService, Data, FriendsService)  {
        TournamentService.all(function(tournaments) {
            $scope.tournaments = tournaments;
        });

        delete Data.currentGame; // So the FriendsControllers show all the friends
        $scope.data = Data;
        $scope.owner = { 'username': UserService.getUsername(), 'id' : UserService.getUserID() };
        $scope.game = { 'classic': true, 'points_exact': 3,  'points_general':  3, 'points_double': 2, 'points_classic': 2, 'open_predictions': true };
        $scope.selectedTournament = {}
        $scope.showOptional = false;

        $scope.gamePoints = {'points_general' : { initial_points : 3, label: 'Resultado General', help : 'Por acertar ganador, perdedor o empate.' },
                             'points_exact' : { initial_points : 3, label: 'Resultado Exacto', classic: false, help : 'Por acertar el resultado exacto.' },
                             'points_double' : { initial_points : 2, label: 'Es Doble', help : 'Por cuanto se multiplica el partido marcado como doble.'  },
                             'points_classic' : { initial_points : 2, label: 'Clasico de la fecha', help : 'Cuantos puntos extras se suman por haber acertado el clasico.' }};

        $scope.newGame = function() {
            var friends = $scope.data.gamePlayerFriends.filter(function(item) { return item.checked });
            var gameplayers = [];

            if(friends.length > 0) {
              gameplayers = friends.map(function(item) { return { 'player': item.id, 'username': item.username, 'initial_points': item.initial_points } });
            }

            gameplayers.push({ 'player': $scope.owner.id, 'username': $scope.owner.username , 'initial_points': $scope.owner.initial_points});

            $scope.game.name  = $scope.game.name; 
            $scope.game.gameplayers =  gameplayers;
            $scope.game.tournament = $scope.selectedTournament.tournament.id;

            $scope.game.points_exact = $scope.gamePoints.points_exact.initial_points;
            $scope.game.points_general = $scope.gamePoints.points_general.initial_points;
            $scope.game.points_double = $scope.gamePoints.points_double.initial_points;
            $scope.game.points_classic = $scope.gamePoints.points_classic.initial_points;

            console.log($scope.game);

            GameService.new($scope.game,
                function(game) {
                    Data.currentGame = game;
                    Data.currentGame.new = true;
                    $location.path('/torneos/detalle/' + game.id);
                },
                function() {
                    console.log("hubo un error");
                });
        };

        $scope.emailFilter = function(value) {
            return !!value.email;
        };

        $scope.steps = [
          {'number': 1, 'label': 'Nombre', validate : function(scope) { return !!scope.game.name; }  },
          {'number': 2, 'label': 'Competicion', validate : function(scope) { return !!scope.selectedTournament.tournament; } },
          {'number': 3, 'label': 'Jugadores'  },
          {'number': 4, 'label': 'Crear Torneo' }
        ];

        $scope.currentStep = $scope.steps[0];
        $scope.optionalStep = {'label' : '?'};

        $scope.setOptionalStep = function() {
          $scope.currentStep = $scope.optionalStep;
        }

        $scope.showAlert = true;
        $scope.hideAlert = function() {
          $scope.showAlert = false;
        };
    }
])

.controller('AddGamePlayersController', ['$scope', 'Facebook', 'Data', 'FriendsService', 'GameService',
    function($scope, Facebook, Data, FriendsService, GameService)  {
        $scope.emailPlayers = [{ email : '' }];
        Data.emailPlayers = $scope.emailPlayers;

        $scope.canInviteMorePlayers = Data.currentGame;

        $scope.addEmailPlayer = function() {
            $scope.emailPlayers.push({email:''});
        };

        $scope.removeEmailPlayer = function(player) {
            var index = $scope.emailPlayers.indexOf(player);
            $scope.emailPlayers.splice(index, 1);
        };

        $scope.withOutFriendsMsg = "No tienes amigos... puedas buscarlos ingresando al";

        /*
        if(Facebook.isAuthenticated()) {
            Facebook.getFriends(
                function(response) {
                    $scope.facebookPlayers = response.data;
                    data.facebookPlayers  = response.data;
                });
        }
        */

        FriendsService.getFriends(
            function(friends) {
                $scope.friends = friends;

                if(!!Data.currentGame) {
                  var gameplayers_ids = Data.currentGame.gameplayers.map(function(e) { return e.player });
                  $scope.friends = friends.filter(function(e) { return gameplayers_ids.indexOf(e.id) < 0 })
                  $scope.withOutFriendsMsg = "No tienes mas amigos para agregar al torneo. Puedes buscar nuevos en el";
                }

                $scope.hasTrueFriends = $scope.friends.filter(function(e) { return e.is_friend }).length > 0;
                Data.gamePlayerFriends = $scope.friends;
            },
            function(error) {
                console.log(error);
            }
        );

        $scope.inviteFriends = function() {
          var friends = $scope.friends.filter(function(f) {  return f.checked && f.is_friend; });
          GameService.inviteFriends($scope.game, friends, 
              function(response) {
                $scope.friends = $scope.friends.filter(function(f) { return !f.checked && f.is_friend; });
                $scope.hasTrueFriends = $scope.friends.length > 0;
                $scope.withOutFriendsMsg = "No tienes mas amigos para agregar al torneo. Puedes buscar nuevos en el";

                for(var i in friends) {
                  var player = friends[i];
                  Data.currentGame.gameplayers.push({ "player": player.id, "username": player.username, "status": null, 'initial_points': player.initial_points })
                }
              }
          );
        }
}])

.controller('DetailGameController', ['$scope', '$routeParams', 'GameService', 'Data', 'UserService',
    function($scope, $routeParams, GameService, Data, UserService)  {
        function setUserStatus(game) {
          $scope.is_owner = game.owner == $scope.username;
          $scope.owner = game.gameplayers.filter(function(p) { return p.username == game.owner })[0];
          $scope.user = game.you[0]
        }

        function setFriendsAnotherChance(game) {
          $scope.friendsAnotherChance = game.gameplayers.filter(function(p) { return !p.status && p.another_chance; });
        }

        $scope.username = UserService.getUsername();

        // We set the current game
        if(!!Data.currentGame && ($routeParams.gameId == Data.currentGame.id)) {
          $scope.game = Data.currentGame;
          $scope.show_message = !!Data.currentGame.new;
          Data.currentGame.new = false;
          setUserStatus($scope.game);
          setFriendsAnotherChance($scope.game);
        } else {

          Data.currentGame = true; 

          GameService.get($routeParams.gameId, 
            function(game) {
              $scope.game = game;
              Data.currentGame = game;
              setUserStatus(game);
              setFriendsAnotherChance($scope.game);
          });
        }

        $scope.updateGamePlayerStatus = function(status) {
            GameService.updateGamePlayerStatus($scope.game.you[0].id, status, 
                function(response) {
                  $scope.user.status = status;
                });
        }

        $scope.updateGamePlayerAnotherChance = function(another_chance) {
            GameService.updateGamePlayerAnotherChance($scope.game.you[0].id, another_chance, 
                function(response) {
                  $scope.user.another_chance = another_chance;
                });
        }

        $scope.invitePlayerAgain = function(gameplayer) {
            GameService.updateGamePlayerInvitePlayerAgain(gameplayer.id,  
                function(response) {
                  gameplayer.status = null;
                });
        }
      
    }
])

.controller('MyGamesController', ['$scope', '$routeParams', 'GameService', 'Data', 'UserService',
    function($scope, $routeParams, GameService, Data, UserService)  {
        GameService.all(function(games) {
          $scope.games = games.filter(function(game) { return  game.you[0].status == true  });
          $scope.hasGames = $scope.games.length > 0;

          if($scope.games.length > 0) {
            $scope.selectGame($scope.games[0]);
          }
        });

        $scope.selectGame = function(game) {
          $scope.selectedGame = game;
          $scope.is_owner = game.owner == $scope.username;
          $scope.owner = game.gameplayers.filter(function(p) { return p.username == game.owner })[0];
          $scope.user = game.you[0];
          $scope.friendsAnotherChance = game.gameplayers.filter(function(p) { return !p.status && p.another_chance; });

          Data.currentGame = game;
        }

        $scope.username = UserService.getUsername();

        $scope.updateGamePlayerStatus = function(status) {
            GameService.updateGamePlayerStatus($scope.game.you[0].id, status, 
                function(response) {
                  $scope.user.status = status;
                });
        }

        $scope.updateGamePlayerAnotherChance = function(another_chance) {
            GameService.updateGamePlayerAnotherChance($scope.game.you[0].id, another_chance, 
                function(response) {
                  $scope.user.another_chance = another_chance;
                });
        }

        $scope.invitePlayerAgain = function(gameplayer) {
            GameService.updateGamePlayerInvitePlayerAgain(gameplayer.id,  
                function(response) {
                  gameplayer.status = null;
                });
        }
      
    }
]);
