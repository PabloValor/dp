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
;
