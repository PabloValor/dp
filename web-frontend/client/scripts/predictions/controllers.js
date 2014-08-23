'use strict';
angular.module('app.predictions')

.controller('PredictionsController', ['$scope', '$q', '$location', 'GameService', 'PredictionService', 'Data',
    function($scope, $q, $location, GameService, PredictionService, Data)  {
        function setTournamentFixture(tournament, currentFixtureNumber) {
            var deferred = $q.defer();
            $scope.loading = true;
            PredictionService.getTournamentFixture($scope.selectedGame.tournament,
              function(tournamentGame) {
                $scope.fixtures = tournamentGame.fixtures;

                var fixture_index = tournamentGame.current_fixture.number;
                if(!!currentFixtureNumber) {
                  fixture_index = currentFixtureNumber;
                } 

                $scope.currentFixture = $scope.fixtures[fixture_index - 1];
                $scope.lastFixtureNumber = tournamentGame.fixtures.length;

                deferred.resolve();

            }, function(error) {
                deferred.reject(error);
            });

            return deferred.promise;
        }

        function setFixturePredictions(gameplayer) {
            var deferred = $q.defer();

            $scope.loading = true;
            PredictionService.getPredictions(gameplayer.id,
              function(predictions) {

                $scope.predictions[gameplayer.id] = predictions;
                deferred.resolve();

            }, function(error) {
                deferred.reject(error);
            });

            return deferred.promise;
        }

        function mapFixturePredictions(fixture, predictions, isClassic) {
          var match;
          var prediction;
          for(var i in fixture.matches) {
            match = fixture.matches[i];

            prediction = predictions[match.id];
            if(!prediction) {
              match.hasPrediction = false;
              continue;
            }

            if(isClassic) {
              if(prediction.local_team_goals > prediction.visitor_team_goals) {
                match.generalPrediction = "local";
              } else if(prediction.local_team_goals < prediction.visitor_team_goals) {
                match.generalPrediction = "visitor";
              } else {
                match.generalPrediction = "draw";
              }
            } else {
                match.predictionLocalGoals = prediction.local_team_goals;
                match.predictionVisitorGoals = prediction.visitor_team_goals;
            }

            match.hasPrediction = prediction.local_team_goals;
          }
        }

        GameService.all(function(games) {
          $scope.games = games.filter(function(game) { return  game.you[0].status == true  });
          $scope.hasGames = $scope.games.length > 0;

          if($scope.games.length > 0) {
            $scope.selectedGame = $scope.games[0];
            setTournamentFixture($scope.selectedGame.tournament)
              .then(function() {
                setFixturePredictions($scope.selectedGame.you[0])
                  .then(function() {
                    var gameplayer = $scope.selectedGame.you[0];
                    mapFixturePredictions($scope.currentFixture, $scope.predictions[gameplayer.id], $scope.selectedGame.classic);
                    $scope.loading = false;
                  });
              })
          }

        });

        $scope.loading = true;
        $scope.predictions = {};

        var lastFixturePositions = {};
        $scope.selectGame = function(game) {

          lastFixturePositions[$scope.selectedGame.name] = $scope.currentFixture.number;
          $scope.selectedGame = game;

          var lastFixturePosition = lastFixturePositions[game.name];
          setTournamentFixture($scope.selectedGame.tournament, lastFixturePosition)
              .then(function() {
                setFixturePredictions($scope.selectedGame.you[0])
                  .then(function() {
                    var gameplayer = $scope.selectedGame.you[0];
                    mapFixturePredictions($scope.currentFixture, $scope.predictions[gameplayer.id], $scope.selectedGame.classic);
                    $scope.loading = false;
                  });
              });
        }

        $scope.nextFixture = function() {
          $scope.currentFixture = $scope.fixtures[$scope.currentFixture.number];
        }

        $scope.previousFixture = function() {
          $scope.currentFixture = $scope.fixtures[$scope.currentFixture.number - 2];
        }

        $scope.doGeneralPrediction = function(match, winner_is_local) {
          var gameplayer = $scope.selectedGame.you[0];
          var local_goals = 0;
          var visitor_goals = 0;

          if(winner_is_local) {
            local_goals = 1;
          } else if(winner_is_local == false) {
            visitor_goals = 1;
          }

          PredictionService.doPrediction(gameplayer.id, match.id, local_goals, visitor_goals);
        }
        
        $scope.doExactPrediction = function(match) {
          var gameplayer = $scope.selectedGame.you[0];
          if(!!match.predictionLocalGoals && !!match.predictionVisitorGoals) {
            PredictionService.doPrediction(gameplayer.id, match.id, match.predictionLocalGoals, match.predictionVisitorGoals);
          }
        }
    }
])
