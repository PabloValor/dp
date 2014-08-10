'use strict';
angular.module('app.games')

.controller('GameController', ['$scope', '$location', 'GameService', 'Data',
    function($scope, $location, GameService, Data)  {
        GameService.all(function(games) {
          $scope.games = games.filter(function(game) { return !( game.you[0].status == false && game.you[0].another_chance == false) });
        });

        $scope.gameDetail = function(game) {
          Data.currentGame = game;
          console.log(game);
          $location.path('/torneos/detalle/' + game.id);
        }

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
        $scope.game = { 'classic': true, 'points_exact': 3,  'points_general':  1, 'points_double': 2, 'points_classic': 2 };

        $scope.gamePoints = {'points_general' : { initial_points : 3, label: 'Resultado General', help : 'Por acertar ganador, perdedor o empate.' },
                             'points_exact' : { initial_points : 1, label: 'Resultado Exacto', classic: false, help : 'Por acertar el resultado exacto.' },
                             'points_double' : { initial_points : 2, label: 'Es Doble', help : 'Por cuanto se multiplica el partido marcado como doble.'  },
                             'points_classic' : { initial_points : 2, label: 'Clasico de la fecha', help : 'Por cuanto se multiplica el clasico de la fecha.' }};

        $scope.newGame = function() {
            var friends = $scope.data.gamePlayerFriends.filter(function(item) { return item.checked });
            var gameplayers = friends.map(function(item) { return { 'player': item.id, 'username': item.username, 'initial_points': item.initial_points } });
            gameplayers.push({ 'player': $scope.owner.id, 'username': $scope.owner.username , 'initial_points': $scope.owner.initial_points});

            $scope.game.name  = $scope.game.name, 
            $scope.game.tournament =  $scope.game.tournament.id;
            $scope.game.gameplayers =  gameplayers;

            $scope.game.points_exact = $scope.gamePoints.points_exact.initial_points;
            $scope.game.points_general = $scope.gamePoints.points_general.initial_points;
            $scope.game.points_double = $scope.gamePoints.points_double.initial_points;
            $scope.game.points_classic = $scope.gamePoints.points_classic.initial_points;

            console.log($scope.game);

            GameService.new($scope.game,
                function(game) {
                    console.log("creado con exito");
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

    }
])

.controller('AddGamePlayersController', ['$scope', 'Facebook', 'Data', 'FriendsService', 'GameService',
    function($scope, Facebook, Data, FriendsService, GameService)  {
        $scope.emailPlayers = [{ email : '' }];
        Data.emailPlayers = $scope.emailPlayers;

        $scope.canInviteMorePlayers = Data.currentGame;

        $scope.addEmailPlayer = function() {
            $scope.emailPlayers.push({email:''});
            console.log($scope.emailPlayers);
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
          console.log(friends);
          GameService.inviteFriends($scope.game, friends, 
              function(response) {
                $scope.friends = $scope.friends.filter(function(f) { return !f.checked && f.is_friend; });
                $scope.hasTrueFriends = $scope.friends.length > 0;
                $scope.withOutFriendsMsg = "No tienes mas amigos para agregar al torneo. Puedes buscar nuevos en el";

                for(var i in friends) {
                  var player = friends[i];
                  Data.currentGame.gameplayers.push({ "player": player.id, "username": player.username, "status": null })
                }
              }
          );
        }
}])

.controller('DetailGameController', ['$scope', '$routeParams', 'GameService', 'Data', 'UserService',
    function($scope, $routeParams, GameService, Data, UserService)  {
        function setUserStatus(game) {
          $scope.is_owner = game.owner == $scope.username;
          $scope.user = game.you[0]
        }

        function setFriendsAnotherChance(game) {
          $scope.friendsAnotherChance = game.gameplayers.filter(function(p) { return !p.status && p.another_chance; });
          console.log("another chance");
          console.log($scope.friendsAnotherChance);
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
                  console.log("response");
                  console.log(response)
                  gameplayer.status = null;
                });
        }
      
    }
]);
