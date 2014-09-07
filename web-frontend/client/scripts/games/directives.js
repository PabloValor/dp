'use strict';
angular.module('app.games')

.directive('gameMode', function() {
    return {
      restrict: 'E',
      templateUrl: 'scripts/games/views/_gameMode.html',
      replace: true,
      scope: { classic: '=' }
    };
})

.directive('gamePoints', function() {
    return {
      restrict: 'E',
      templateUrl: 'scripts/games/views/_gamePoints.html',
      replace: true,
      scope: { game: '=' }
    };
})

.directive('gameOpen', function() {
    return {
      restrict: 'E',
      templateUrl: 'scripts/games/views/_gameOpen.html',
      replace: true,
      scope: { open: '=' }
    };
})

.directive('newGameWizard', function() {
    return {
      restrict: 'E',
      templateUrl: 'scripts/games/views/_newGameWizard.html',
      transclude: true,
      scope: { steps: '=', 
               currentStep : '=', 
               optionalStep: '=', 
               showOptional: '=', 
               action: '=', 
               game: '=', 
               selectedTournament: '='},
      link: function($scope, element, attrs) {

        $scope.lastStep = $scope.steps[$scope.steps.length - 1];
        $scope.showOptional = false;

        $scope.nextStep = function() {
          var index = $scope.steps.indexOf($scope.currentStep);
          $scope.currentStep = $scope.steps[index + 1];
        };

        $scope.previousStep = function() {
          var index = $scope.steps.indexOf($scope.currentStep);
          $scope.currentStep = $scope.steps[index - 1];
        };

        $scope.setlastStep = function() {
          $scope.showOptional = false;
          $scope.currentStep = $scope.lastStep;
        };

        $scope.setOptionalStep = function() {
          $scope.showOptional = true;
        };

        $scope.finish = function() {
          $scope.action();
        }

        $scope.validate = function() {
          if($scope.currentStep.validate) {
            return $scope.currentStep.validate($scope);
          } else {
            return true;
          }
        }
      }
    };
})

.directive('gameTable', function() {
    return {
      restrict: 'E',
      templateUrl: 'scripts/games/views/_gameTable.html',
      replace: true
    };
})

.directive('gameTableWide', function() {
    return {
      restrict: 'E',
      templateUrl: 'scripts/games/views/_gameTableWide.html',
      replace: true
    };
})

.directive('gameTableFixturePoints', function() {
    return {
      restrict: 'E',
      templateUrl: 'scripts/games/views/_gameTableFixturePoints.html',
      replace: true
    };
})

.directive('gameTableFixturePointsWide', function() {
    return {
      restrict: 'E',
      templateUrl: 'scripts/games/views/_gameTableFixturePointsWide.html',
      replace: true
    };
})

.directive('gameTableChart', function() {
    return {
      restrict: 'E',
      templateUrl: 'scripts/games/views/_gameTableChart.html',
      replace: true,
      scope: {fixturePoints : '=', gameplayers : '=' },
      controller: function($scope) {
        var fixture_points_data = [];
        var gp_points_total = {};
        var points,
            old_points,
            fp_data,
            fp,
            gp_username;

        for(var f in $scope.fixturePoints) {
          fp = $scope.fixturePoints[f];
          fp_data = {'fixture': f };

          for(var i in $scope.gameplayers) {
            gp_username = $scope.gameplayers[i];
            points = 0;

            // If the player played that fixture
            // We search for his fixture points
            if(!!fp[gp_username]) {
              points = fp[gp_username].points;
            }

            old_points = 0;
            if(!!gp_points_total[gp_username]) {
              old_points = gp_points_total[gp_username];
            }

            fp_data[gp_username] = points + old_points;
            gp_points_total[gp_username] = points + old_points;
          }

          fixture_points_data.push(fp_data);
        }

        $scope.fixture_points_data = fixture_points_data;

      }
    };
})

.directive('tournamentTable', function() {
    return {
      restrict: 'E',
      templateUrl: 'scripts/games/views/_tournamentTable.html',
      replace: true
    };
})

;

