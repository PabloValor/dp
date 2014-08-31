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
      replace: true,
      scope: { game: '=', username: '=' },
      controller: function($scope) {


        // Player Total Points
        var gp, fp, gp_points;
        var gameplayers_points = [];

        for(var i in $scope.game.gameplayers) {
          gp = $scope.game.gameplayers[i];
          gp_points = 0;

          for(var j in gp.fixture_points) {
            fp = gp.fixture_points[j];
            gp_points += fp.points;
          }

          gameplayers_points.push({ 'username': gp.username, 'points': gp_points });
        }

        $scope.gameplayer_points = gameplayers_points;
      }
    };
})
;
