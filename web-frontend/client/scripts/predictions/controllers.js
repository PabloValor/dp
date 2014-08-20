'use strict';
angular.module('app.predictions')

.controller('PredictionsController', ['$scope', '$location', 'GameService', 'PredictionService', 'Data',
    function($scope, $location, GameService, PredictionService, Data)  {
        function setTournamentFixture(tournament, currentFixtureNumber) {
            $scope.loading = true;
            PredictionService.getTournamentFixture($scope.selectedGame.tournament,
              function(tournamentGame) {
                $scope.fixtures = tournamentGame.fixtures;

                var fixture_index = tournamentGame.current_fixture.number;
                if(!!currentFixtureNumber) {
                  fixture_index = currentFixtureNumber;
                } 

                $scope.currentFixture = $scope.fixtures[fixture_index - 1];
                console.info($scope.currentFixture);
                $scope.lastFixtureNumber = tournamentGame.fixtures.length;
                $scope.loading = false;
            });
        }

        GameService.all(function(games) {
          $scope.games = games.filter(function(game) { return  game.you[0].status == true  });
          $scope.hasGames = $scope.games.length > 0;

          if($scope.games.length > 0) {
            $scope.selectedGame = $scope.games[0];
            console.info($scope.selectedGame);
            setTournamentFixture($scope.selectedGame.tournament);
          }

        });

        $scope.loading = true;

        var lastFixturePositions = {};
        $scope.selectGame = function(game) {
          console.info(game);
          console.info(lastFixturePositions);

          lastFixturePositions[$scope.selectedGame.name] = $scope.currentFixture.number;
          $scope.selectedGame = game;

          var lastFixturePosition = lastFixturePositions[game.name];
          setTournamentFixture($scope.selectedGame.tournament, lastFixturePosition);
        }

        $scope.nextFixture = function() {
          $scope.currentFixture = $scope.fixtures[$scope.currentFixture.number];
        }

        $scope.previousFixture = function() {
          $scope.currentFixture = $scope.fixtures[$scope.currentFixture.number - 2];
        }
    }
])
