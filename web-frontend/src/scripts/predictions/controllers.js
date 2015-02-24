'use strict';
angular.module('app.predictions')

.controller('PredictionsController', ['$scope', '$q', '$location', 'GameService', 'PredictionService', 'Data', '$rootScope', 'logger',
    function($scope, $q, $location, GameService, PredictionService, Data, $rootScope, logger)  {
        function setTournamentFixture(tournament, currentFixtureNumber) {
            var deferred = $q.defer();
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

            PredictionService.getPredictions(gameplayer.id,
              function(predictions) {

                console.info("Predictions");
                console.info(predictions);
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
          fixture.points = 0;
          for(var i in fixture.matches) {
            match = fixture.matches[i];

            prediction = predictions[match.id];
            if(!prediction) {
              delete match.generalPrediction;
              delete match.predictionLocalGoals;
              delete match.predictionVisitorGoals;
              match.hasPrediction = false;
              match.points = 0;
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

            match.hasPrediction = true;
            match.points = prediction.points;
            fixture.points += prediction.points;
          }
        }

        $scope.showPage = false;

        GameService.all(function(games) {
          $scope.games = games.filter(function(game) { return  game.you[0].status == true  });
          $scope.hasGames = $scope.games.length > 0;

          $scope.showPage = true;
          if($scope.hasGames) {
            $scope.selectedGame = $scope.games[0];
            $scope.selectedGameplayer = $scope.selectedGame.you[0];
            $scope.userGameplayer =$scope.selectedGame.you[0];

            setTournamentFixture($scope.selectedGame.tournament)
              .then(function() {
                setFixturePredictions($scope.selectedGame.you[0])
                  .then(function() {
                    var gameplayer = $scope.selectedGame.you[0];
                    mapFixturePredictions($scope.currentFixture, $scope.predictions[gameplayer.id], $scope.selectedGame.classic);
                    $rootScope.loadingInit = false;
                  });
              })
          } else {
            $rootScope.loadingInit = false;
          }

        }, function(response) {
          console.error(response);
          $rootScope.loadingInit = false;
        });

        $rootScope.loadingInit = true;
        $scope.loadingFixture = false;
        $scope.predictions = {};

        var lastFixturePositions = {};
        $scope.selectGame = function(game) {

          lastFixturePositions[$scope.selectedGame.name] = $scope.currentFixture.number;
          $scope.selectedGame = game;
          $scope.selectedGameplayer = $scope.selectedGame.you[0];
          $scope.userGameplayer = $scope.selectedGame.you[0];


          $scope.loadingFixture = true;
          var lastFixturePosition = lastFixturePositions[game.name];
          setTournamentFixture($scope.selectedGame.tournament, lastFixturePosition)
              .then(function() {
                setFixturePredictions($scope.selectedGame.you[0])
                  .then(function() {
                    var gameplayer = $scope.selectedGame.you[0];
                    mapFixturePredictions($scope.currentFixture, $scope.predictions[gameplayer.id], $scope.selectedGame.classic);
                    $scope.loadingFixture = false;
                  });
              });
        }

        $scope.selectGameplayer = function(gameplayer) {
          $scope.loadingFixture = true;
          $scope.selectedGameplayer = gameplayer;

          setFixturePredictions(gameplayer)
            .then(function() {
              mapFixturePredictions($scope.currentFixture, $scope.predictions[gameplayer.id], $scope.selectedGame.classic);
              $scope.loadingFixture = false;
            });
        }

        $scope.nextFixture = function() {
          $scope.currentFixture = $scope.fixtures[$scope.currentFixture.number];
          mapFixturePredictions($scope.currentFixture, $scope.predictions[$scope.selectedGameplayer.id], $scope.selectedGame.classic);
        }

        $scope.previousFixture = function() {
          $scope.currentFixture = $scope.fixtures[$scope.currentFixture.number - 2];
          mapFixturePredictions($scope.currentFixture, $scope.predictions[$scope.selectedGameplayer.id], $scope.selectedGame.classic);
        }

        $scope.doGeneralPrediction = function(match, winner_is_local) {
          var gameplayer = $scope.selectedGame.you[0];
          var local_goals = 0;
          var visitor_goals = 0;

          var old_prediction = match.generalPrediction;

          if(winner_is_local) {
            local_goals = 1;
            match.generalPrediction = "local";
          } else if(winner_is_local == false) {
            visitor_goals = 1;
            match.generalPrediction = "visitor";
          } else {
            match.generalPrediction = "draw";
          }

          PredictionService.doPrediction(gameplayer.id, match.id, local_goals, visitor_goals, 
              function(prediction) {
                match.hasPrediction = true;
                $scope.predictions[$scope.selectedGameplayer.id][match.id ] = prediction;
              },
              function(error) {
                  logger.logError("Ha surgido un error, por favor intentelo de vuelta.");
                  match.generalPrediction = old_prediction;
              });
        }
        
        $scope.doExactPrediction = function(match) {
          var gameplayer = $scope.selectedGame.you[0];
          if(!!match.predictionLocalGoals && !!match.predictionVisitorGoals) {
            PredictionService.doPrediction(gameplayer.id, match.id, match.predictionLocalGoals, match.predictionVisitorGoals, 
                function(prediction) {
                  match.hasPrediction = true;
                  $scope.predictions[$scope.selectedGameplayer.id][match.id ] = prediction;
                });
          }
        }
    }
])
