'use strict';
angular.module('app.predictions')

.factory('PredictionService', ['$http', 'SETTINGS','Data', 
    function($http, SETTINGS, Data) {
      var tournaments = {};

      return {
          getTournamentFixture: function(tournament_id,f_success, f_error) {
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
                                }
    }
}]);
