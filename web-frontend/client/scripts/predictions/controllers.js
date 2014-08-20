'use strict';
angular.module('app.predictions')

.controller('PredictionsController', ['$scope', '$location', 'GameService', 'PredictionService', 'Data',
    function($scope, $location, GameService, PredictionService, Data)  {
        function setTournamentFixture(tournament, currentFixtureNumber) {
            $scope.loading = true;
            PredictionService.getTournamentFixture($scope.selectedGame.tournament,
              function(tournamentGame) {
                $scope.fixtures = tournamentGame.fixtures;
                if(!!currentFixtureNumber) {
                  $scope.currentFixtureNumber = currentFixtureNumber;
                } else {
                  $scope.currentFixtureNumber = tournamentGame.current_fixture.number;
                }

                $scope.lastFixtureNumber = tournamentGame.fixtures.length;
                $scope.loading = false;
            });
        }

        GameService.all(function(games) {
          $scope.games = games.filter(function(game) { return  game.you[0].status == true  });
          $scope.hasGames = $scope.games.length > 0;

          if($scope.games.length > 0) {
            $scope.selectedGame = $scope.games[0];
            console.log($scope.selectedGame);
            setTournamentFixture($scope.selectedGame.tournament);
          }

        });

        $scope.loading = true;

        var lastFixturePositions = {};
        $scope.selectGame = function(game) {
          console.log(game);
          console.log(lastFixturePositions);

          lastFixturePositions[$scope.selectedGame.name] = $scope.currentFixtureNumber;
          $scope.selectedGame = game;

          var lastFixturePosition = lastFixturePositions[game.name];
          setTournamentFixture($scope.selectedGame.tournament, lastFixturePosition);
        }

        $scope.nextFixture = function() {
          $scope.currentFixtureNumber += 1;
        }

        $scope.previousFixture = function() {
          $scope.currentFixtureNumber -= 1;
        }
    }
])
