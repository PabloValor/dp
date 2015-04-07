'use strict';
angular.module('app.predictions')

.factory('PredictionService', ['$http', 'SETTINGS','Data', 
    function($http, SETTINGS, Data) {
      var tournaments = {};
      var predictions = {};
      var fixtures = {};

      return {
          getTournamentFixture: 
                function(tournament_id,f_success, f_error) {
                  var tournament = tournaments[tournament_id]; 
                  if(!!tournament) {
                    f_success(tournament);
                    return;
                  }

                  $http.get(SETTINGS.url.tournamentFixture(tournament_id))
                  .success(function(response) {
                      tournaments[tournament_id] = response;
                      console.log(response)

                      if(!!f_success) {
                          f_success(response);
                      }
                  })
                  .error(function(response) {
                      console.log(response);

                      if(!!f_error) {
                          f_success(response);
                      }
                  });
                },
          getFixtureByNumber: 
                function(tournament_id, fixture_number, f_success, f_error) {
                  var tournament = fixtures[tournament_id];
                  if(!!tournament) {
                    var fixture = fixtures[tournament_id][fixture_number];

                    if(!!fixture) {
                      if(!!f_success)
                        f_success(fixture);
                      return;
                    }

                  } else {
                    fixtures[tournament_id] = {};
                  }

                  $http.get(SETTINGS.url.fixtureByNumber(tournament_id, fixture_number))
                  .success(function(response) {
                      fixtures[tournament_id][fixture_number] = response;

                      if(!!f_success) {
                          f_success(response);
                      }
                  })
                  .error(function(response) {
                      console.log(response);

                      if(!!f_error) {
                          f_success(response);
                      }
                  });
                },          
            doPrediction: 
                function(gameplayer_id, match_id, local_team_goals, visitor_team_goals, f_success, f_error) {
                  var data = {'gameplayer': gameplayer_id, 
                              'match': match_id, 
                              'local_team_goals': local_team_goals, 
                              'visitor_team_goals': visitor_team_goals };

                  console.info('Do Predictions');
                  $http.post(SETTINGS.url.doPrediction(), data)
                  .success(function(response) {
                      console.info(response);

                      if(!!f_success) {
                          f_success(response);
                      }
                  })
                  .error(function(response) {
                      console.error(response);

                      if(!!f_error) {
                          f_error(response);
                      }
                  });
                },
            getPredictions: 
                function(gameplayer_id, f_success, f_error) {
                  $http.get(SETTINGS.url.getPredictions(gameplayer_id))
                  .success(function(predictions) {
                      var matches_predictions = {};
                      var prediction;
                      for(var i in predictions) {
                          prediction = predictions[i];
                          matches_predictions[prediction.match.id] = prediction;
                      }

                      if(!!f_success) {
                          f_success(matches_predictions);
                      }
                  })
                  .error(function(response) {
                      console.log("ERROR");
                      console.error(response);

                      if(!!f_error) {
                          f_error(response);
                      }
                  });
                },
            getPredictionsByFixtureNumber: 
                function(gameplayer_id, fixture_number,  f_success, f_error) {
                  $http.get(SETTINGS.url.getPredictionsByFixtureNumber(gameplayer_id, fixture_number))
                  .success(function(predictions) {
                      var matches_predictions = {};
                      var prediction;
                      for(var i in predictions) {
                          prediction = predictions[i];
                          matches_predictions[prediction.match.id] = prediction;
                      }

                      if(!!f_success) {
                          f_success(matches_predictions);
                      }
                  })
                  .error(function(response) {
                      console.log("ERROR");
                      console.error(response);

                      if(!!f_error) {
                          f_error(response);
                      }
                  });
                }
    }
}]);
