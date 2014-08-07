'use strict';
angular.module('app.games')

.controller('GameController', ['$scope', '$location', 'GameService', 'Data',
    function($scope, $location, GameService, Data)  {
        GameService.all(function(games) {
          $scope.games = games;
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

          return (filter == "playing" && status ) ||
                 (filter == "waiting" && status == undefined) ||
                 (filter == "rejected" && status == false) ||
                 (filter == "");
        };
    }
])

.controller('NewGameController', ['$scope', '$location', 'TournamentService', 'GameService', 'Facebook', 'UserService', 'Data', 'FriendsService',
    function($scope, $location, TournamentService, GameService, Facebook, UserService, Data, FriendsService)  {
        TournamentService.all(function(tournaments) {
            $scope.tournaments = tournaments;
        });

        $scope.owner = UserService.getUsername();
        $scope.emailPlayers = [{ email : '' }];

        $scope.addEmailPlayer = function() {
            $scope.emailPlayers.push({email:''});
            console.log($scope.emailPlayers);
        };
        $scope.emailFilter = function(value) {
            return !!value.email;
        };

        $scope.removeEmailPlayer = function(player) {
            var index = $scope.emailPlayers.indexOf(player);
            $scope.emailPlayers.splice(index, 1);
        };

        if(Facebook.isAuthenticated()) {
            Facebook.getFriends(
                function(response) {
                    $scope.facebookPlayers = response.data;
                    console.log(response);
                });
        }

        FriendsService.getFriends(
                function(friends) {
                    $scope.friends = friends;
                },
                function(error) {
                    console.log(error);
                }
        );

        $scope.newGame = function() {
            var friends = $scope.friends.filter(function(item) { return item.checked });
            var gameplayers = friends.map(function(item) { return { 'player': item.id, 'username': item.username } });
            var game = {'name' : $scope.game.name, 'tournament': $scope.game.tournament.id, 'gameplayers': gameplayers};

            GameService.new(game,
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
    }
])

.controller('DetailGameController', ['$scope', '$routeParams', 'GameService', 'Data', 'UserService',
    function($scope, $routeParams, GameService, Data, UserService)  {
        function setUserStatus(game) {
          $scope.is_owner = game.owner == $scope.username;
          $scope.user = game.you[0]
        }

        $scope.username = UserService.getUsername();

        if(!!Data.currentGame) {
          $scope.game = Data.currentGame;
          $scope.show_message = !!Data.currentGame.new;
          Data.currentGame.new = false;
          setUserStatus($scope.game);

        } else {
          GameService.get($routeParams.gameId, 
            function(game) {
              $scope.game = game;
              setUserStatus(game);
          });
        }

        $scope.updateGamePlayerStatus = function(status) {
            GameService.updateGamePlayerStatus($scope.game.you[0].id, status, 
                function(response) {
                  $scope.user.status = status;
                });
        }
      
    }
]);
