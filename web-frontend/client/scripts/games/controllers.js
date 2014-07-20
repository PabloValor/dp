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
            var gameplayers = friends.map(function(item) { return { 'player': item.id } });

            GameService.new({'name' : $scope.game.name, 'tournament': $scope.game.tournament.id, 'gameplayers': gameplayers},
                function() {
                    console.log("creado con exito");
                },
                function() {
                    console.log("hubo un error");
                });
        };
    }
]);
