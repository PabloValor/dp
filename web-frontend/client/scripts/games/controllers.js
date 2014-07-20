'use strict';
angular.module('app.games')

.controller('GameController', ['$scope', 'GameService', 
    function($scope, GameService)  {
        $scope.games = GameService.all();
    }
])

.controller('NewGameController', ['$scope', 'TournamentService', 'GameService', 'Facebook', 'UserService',
    function($scope, TournamentService, GameService, Facebook, UserService)  {
        TournamentService.all(function(tournaments) {
            $scope.tournaments = tournaments;
        });

        $scope.emailPlayers = [{email:''}];
        $scope.addEmailPlayer = function() {
            $scope.emailPlayers.push({email:''});
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
            GameService.new({'name' : $scope.game.name, 'tournament': $scope.game.tournament.id },
                function() {
                    console.log("creado con exito");
                },
                function() {
                    console.log("hubo un error");
                });
        };
    }
]);
