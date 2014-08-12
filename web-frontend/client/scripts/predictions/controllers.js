'use strict';
angular.module('app.predictions')

.controller('PredictionsController', ['$scope', '$location', 'GameService', 'Data',
    function($scope, $location, GameService, Data)  {
        GameService.all(function(games) {
          $scope.games = games.filter(function(game) { return  game.you[0].status == true  });
          $scope.hasGames = $scope.games.length > 0;
          console.log($scope.hasGames);

          if($scope.games.length > 0) {
            $scope.selectedGame = $scope.games[0];
            console.log($scope.selectedGame);

          }
        });

        $scope.selectGame = function(game) {
          $scope.selectedGame = game;
        }
    }
])
