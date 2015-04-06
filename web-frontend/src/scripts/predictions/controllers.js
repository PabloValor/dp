'use strict';
angular.module('app.predictions')

.controller('PredictionsController', ['$scope', '$q', '$location', 'GameService', 'PredictionService', 'Data', '$rootScope', 'logger',
    function($scope, $q, $location, GameService, PredictionService, Data, $rootScope, logger)  {
        function changeCurrentFixture(tournament_id, fixture_number, f_success) {
          if(!!!f_success) {
            $scope.loadingFixture = true;
          }
          
          setCurrentFixture(tournament_id, fixture_number)
              .then(function() {
                setFixturePredictions($scope.selectedGame.you[0])
                  .then(function() {
                    var gameplayer = $scope.selectedGame.you[0];
                    mapFixturePredictions($scope.currentFixture, $scope.predictions[gameplayer.id], $scope.selectedGame.classic);

                    if(!!!f_success) {
                      $scope.loadingFixture = false;
                    }

                    if(!!f_success) {
                      f_success();
                    }
                  });
              });

          if(fixture_number > 0) {
            PredictionService.getFixtureByNumber(tournament_id, fixture_number + 1);
          }

          PredictionService.getFixtureByNumber(tournament_id, fixture_number - 1);
        }

        function setCurrentFixture(tournament_id, fixture_number) {
            var deferred = $q.defer();
            PredictionService.getFixtureByNumber(tournament_id, fixture_number,
              function(fixture) {
                $scope.currentFixture = fixture;

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
        $scope.predictions = {};
        $rootScope.loadingInit = true;

        GameService.all(function(games) {
          $scope.games = games.filter(function(game) { return  game.you[0].status == true  });
          $scope.hasGames = $scope.games.length > 0;

          $scope.showPage = true;
          if($scope.hasGames) {
            $scope.selectedGame = $scope.games[0];
            $scope.selectedGameplayer = $scope.selectedGame.you[0];
            $scope.userGameplayer =$scope.selectedGame.you[0];

            var fixture_number = $scope.selectedGame.current_fixture.number;
            var tournament_id = $scope.selectedGame.tournament_id;

            changeCurrentFixture(tournament_id, fixture_number, function() { $rootScope.loadingInit = false; });

          } else {
            $rootScope.loadingInit = false;
          }

        }, function(response) {
          console.error(response);
          $rootScope.loadingInit = false;
        });

        $scope.selectGame = function(game) {
          $scope.selectedGame = game;
          $scope.selectedGameplayer = $scope.selectedGame.you[0];
          $scope.userGameplayer = $scope.selectedGame.you[0];

          var fixture_number = $scope.selectedGame.current_fixture.number;
          var tournament_id = $scope.selectedGame.tournament_id;
          changeCurrentFixture(tournament_id, fixture_number);
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
          var fixture_number = $scope.currentFixture.number + 1;
          var tournament_id = $scope.selectedGame.tournament_id;
          changeCurrentFixture(tournament_id, fixture_number);
        }

        $scope.previousFixture = function() {
          var fixture_number = $scope.currentFixture.number - 1;
          var tournament_id = $scope.selectedGame.tournament_id;
          changeCurrentFixture(tournament_id, fixture_number);
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
