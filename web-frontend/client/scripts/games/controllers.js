'use strict';
angular.module('app.games')

.controller('GameController', ['$scope', 'GameService', 
    function($scope, GameService)  {
        GameService.all(function(playergames) {
          $scope.playergames = playergames;
        });

    }
])

.controller('NewGameController', ['$scope', '$location', 'TournamentService', 'GameService', 'Facebook', 'UserService', 'Data',
    function($scope, $location, TournamentService, GameService, Facebook, UserService, Data)  {
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

        UserService.getFriends(
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
                    $location.path('/torneo/' + game.id);
                },
                function() {
                    console.log("hubo un error");
                });
        };
    }
])

.controller('DetailGameController', ['$scope', '$routeParams', 'GameService', 'Data',
    function($scope, $routeParams, GameService, Data)  {
        if(!!Data.currentGame && Data.currentGame.new) {
          $scope.game = Data.currentGame;
          $scope.show_message = true;
          Data.currentGame.new = false;
        } else {
          GameService.get($routeParams.gameId, 
            function(game) {
              $scope.game = game;
          });
        }
      
    }
]);
